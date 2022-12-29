from twitchio.ext import commands


class QueueCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
