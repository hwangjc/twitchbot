from twitchio.ext import commands
from secret import TOKEN, CLIENT_ID, CHANNEL
from user_commands import UserCommand, UserCommandUtils

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, client_secret=CLIENT_ID, prefix="!", initial_channels=[CHANNEL])
        self.user_commands_file = "persistent/usercommands"
    
    async def event_ready(self):
        print(f"{self.nick} ready")

    async def is_mod(self, ctx):
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
        UserCommandUtils.encode_to_file(
            command=new_cmd, 
            file_name=self.user_commands_file
        )
        print(f"Command: {new_cmd_name} persisted")
