from twitchio.ext import commands

import shutil
from threading import Thread, Lock
from typing import List


class UserCmdAlreadyExistsEx(Exception):
    """Exception raised user commands already exist."""
    pass


class UserCmdDoesNotExistEx(Exception):
    """Exception a user commands does not exist."""
    pass


class UserCommand:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class UserCommandUtils:
    @staticmethod
    def user_command_to_twitch_command(
        user_command: UserCommand
    ) -> commands.Command:
        # Make temporary Callable that since Python doesn't have "async lambdas"
        async def temp_user_command(ctx: commands.Context):
            await ctx.send(user_command.content)

        return commands.Command(
            name=user_command.name[1:],  # 1 to end to remove command prefix
            func=temp_user_command
        )


class UserCommandFileUtils:
    DELIM = "&&&"

    @staticmethod
    def __encode_command(command: UserCommand) -> str:
        return f"{command.name}{UserCommandFileUtils.DELIM}{command.content}\n"

    @staticmethod
    def __decode_line(encoded: str) -> UserCommand:
        parts = encoded.split(UserCommandFileUtils.DELIM, 2)
        name = parts[0]
        content = parts[1][:-1]  # Remove the newline character during encoding
        return UserCommand(name, content)

    @staticmethod
    def encode_to_file(
        command: UserCommand, 
        file_name: str,
        file_lock: Lock,
    ) -> None:
        file_lock.acquire()
        with open(file_name, "a") as file:
            file.write(UserCommandFileUtils.__encode_command(command))
        file_lock.release()
        print(f"Command: {command.name} persisted")

    @staticmethod
    def encode_all_to_file(
        commands: List[UserCommand], 
        file_name: str,
        file_lock: Lock
    ) -> None:
        # Write to temporary file
        tmp_file_name = f"{file_name}_tmp"
        open(tmp_file_name, "w").close()
        with open(tmp_file_name, "a") as tmp_file:
            for command in commands:
                tmp_file.write(UserCommandFileUtils.__encode_command(command))

        # Overwrite actual file with temp file
        file_lock.acquire()
        shutil.move(tmp_file_name, file_name)
        file_lock.release()
        print("All persisted")

    @staticmethod
    def decode_from_file(file_name: str, file_lock: Lock) -> List[UserCommand]:
        cmds = []
        file_lock.acquire()
        with open(file_name, "r") as file:
            while True:
                encoded = file.readline()
                if len(encoded) == 0:
                    break
                decoded = UserCommandFileUtils.__decode_line(encoded)
                print(f"Command: {decoded.name} decoded")
                cmds.append(decoded)
        file_lock.release()
        return cmds


class UserCommandManager:
    def __init__(self, bot: commands.Bot, persistent_file_name: str):
        self.bot = bot
        self.file_name = persistent_file_name
        # user_commands is a map of commmand name -> UserCommand object
        self.user_commands: dict[str, UserCommand] = {}
        # Didn't want to implement reader writer locks in Python so just
        # using a basic mutex for now. Less efficient on reads but whatever.
        # uc_lock is used for locking self.user_commands
        # file_lock is used for the persistent file
        self.uc_lock = Lock()
        self.file_lock = Lock()
    
    def init_user_commands(self) -> None:
        self.uc_lock.acquire()
        user_commands = UserCommandFileUtils.decode_from_file(
            self.file_name,
            self.file_lock
        ) 
        for command in user_commands:
            self.user_commands[command.name] = command
            self.bot.add_command(
                UserCommandUtils.user_command_to_twitch_command(
                    command
                )
            )
            print(f"Command: {command.name} loaded")
        self.uc_lock.release()

    def add_user_command(self, command: UserCommand) -> None:
        self.uc_lock.acquire()
        # See if this command already exists
        if command.name in self.user_commands:
            self.uc_lock.release()
            raise UserCmdAlreadyExistsEx

        # Save new command to file
        UserCommandFileUtils.encode_to_file(
            command=command, 
            file_name=self.file_name,
            file_lock=self.file_lock
        )

        # Save new command to UCM memory
        self.user_commands[command.name] = command
        self.uc_lock.release()

        # Load command
        self.bot.add_command(
            UserCommandUtils.user_command_to_twitch_command(command)
        )

    def rm_user_command(self, command_name: str) -> None:
        self.uc_lock.acquire()
        # Make sure command exists
        if command_name not in self.user_commands:
            self.uc_lock.release()
            raise UserCmdDoesNotExistEx

        # Remove from UCM memory
        del self.user_commands[command_name]

        # Write new UCM memory to file, but do this in a separate thread because
        # overwriting files is dumb inefficient
        t = Thread(
            target=UserCommandFileUtils.encode_all_to_file,
            args=(list(self.user_commands.values()), self.file_name, self.file_lock)
        )
        t.start()
        # Wait for the thread to finish executing to release the uc_lock, otherwise
        # there could be an inconsistency between in memory UCM and persistent file.
        t.join()
        self.uc_lock.release()

        # Remove command
        try:
            self.bot.remove_command(command_name[1:])
        except commands.errors.CommandNotFound as e:
            # This shouldn't happen, and if it does, something is very wrong
            raise UserCmdDoesNotExistEx("Something went horribly wrong")
