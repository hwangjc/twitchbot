from twitchio.ext import commands

from secret import TOKEN, CLIENT_ID, CHANNEL
from user_commands import (
    UserCommand,
    UserCommandManager,
    UserCmdAlreadyExistsEx,
    UserCmdDoesNotExistEx,
)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, client_secret=CLIENT_ID, prefix="!", initial_channels=[CHANNEL])
        self.user_commands_file = "persistent/usercommands"
        self.ucm = UserCommandManager(bot=self, persistent_file_name=self.user_commands_file)
    
    async def event_ready(self):
        print(f"{self.nick} ready")

    def init_user_commands(self):
        self.ucm.init_user_commands()

    async def is_mod(self, ctx) -> bool:
        if not ctx.author.is_mod:
            await ctx.reply("lol not a mod")
        return ctx.author.is_mod

    @commands.command(name="addcommand")
    async def addcommand(self, ctx: commands.Context):
        if not await self.is_mod(ctx):
            return
        # Parse message
        msg_parts = ctx.message.content.split(" ", 2)
        if len(msg_parts) != 3:
            return
        new_cmd_name = msg_parts[1]
        new_cmd_content = msg_parts[2]

        # Save new command
        new_cmd = UserCommand(new_cmd_name, new_cmd_content)
        try:
            self.ucm.add_user_command(new_cmd)
            await ctx.send(f"Command: {new_cmd_name} added successfully")
        except UserCmdAlreadyExistsEx as e:
            await ctx.send(f"Command: {new_cmd_name} already exists")

    @commands.command(name="rmcommand")
    async def rmcommand(self, ctx: commands.Context):
        if not await self.is_mod(ctx):
            return
        # Parse
        msg_parts = ctx.message.content.split(" ", 1)
        if len(msg_parts) != 2:
            return
        sad_cmd_name = msg_parts[1]

        # Remove command
        try:
            self.ucm.rm_user_command(sad_cmd_name)
            await ctx.send(f"Command: {sad_cmd_name} removed successfully")
        except UserCmdDoesNotExistEx as e:
            await ctx.send(f"Command: {sad_cmd_name} does not exist")
