from twitchio.ext import commands

from errors import UserCmdExistsError, UserCmdDNEError
from secret import TOKEN, CLIENT_ID, CHANNEL
from user_commands import UserCommand, UserCommandManager
from utils import UserUtils


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN, 
            client_secret=CLIENT_ID, 
            prefix="!", 
            initial_channels=[CHANNEL]
        )
        self.broadcaster_name = CHANNEL
        self.user_commands_file = "persistent/usercommands"
        self.ucm = UserCommandManager(
            bot=self, persistent_file_name=self.user_commands_file
        )
    
    async def event_ready(self):
        print(f"{self.nick} ready")

    def init_user_commands(self):
        self.ucm.init_user_commands()

    @commands.command(name="addcommand")
    async def addcommand(
        self, 
        ctx: commands.Context, 
        new_cmd_name: str, 
        *args
    ):
        if not await UserUtils.is_mod_author(ctx):
            return
        # Save new command
        new_cmd = UserCommand(new_cmd_name, " ".join(args))
        try:
            self.ucm.add_user_command(new_cmd)
            await ctx.send(f"Command: {new_cmd_name} added successfully")
        except UserCmdExistsError as e:
            await ctx.send(f"Command: {new_cmd_name} already exists")

    @commands.command(name="rmcommand")
    async def rmcommand(self, ctx: commands.Context, sad_cmd_name: str):
        if not await UserUtils.is_mod_author(ctx):
            return
        # Remove command
        try:
            self.ucm.rm_user_command(sad_cmd_name)
            await ctx.send(f"Command: {sad_cmd_name} removed successfully")
        except UserCmdDNEError as e:
            await ctx.send(f"Command: {sad_cmd_name} does not exist")

    @commands.command(name="editcommand")
    async def editcommand(
        self, 
        ctx: commands.Context,
        cmd_name: str,
        *args
    ):
        if not await UserUtils.is_mod_author(ctx):
            return
        # Edit command
        try:
            self.ucm.edit_user_command(cmd_name, " ".join(args))
            await ctx.send(f"Command: {cmd_name} was updated successfully")
        except UserCmdDNEError as e:
            await ctx.send(f"Command: {cmd_name} does not exist")

