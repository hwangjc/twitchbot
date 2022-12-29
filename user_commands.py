from typing import List

class UserCommand:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

class UserCommandUtils:
    DELIM = "&&&"

    @staticmethod
    def encode_to_file(command: UserCommand, file_name: str) -> None:
        with open(file_name, "a") as file:
            file.write(f"{command.name}{UserCommandUtils.DELIM}{command.content}\n")

    @staticmethod
    def decode_from_file(file_name: str) -> List[UserCommand]:
        cmds = []
        with open(file_name, "r") as file:
            while True:
                encoded = file.readline()
                if len(encoded) == 0:
                    break
                cmds.append(UserCommandUtils.__decode_line(encoded))
        return cmds
    
    @staticmethod
    def __decode_line(encoded: str) -> UserCommand:
        parts = encoded.split(UserCommandUtils.DELIM, 2)
        return UserCommand(parts[0], parts[1])
