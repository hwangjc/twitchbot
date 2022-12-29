from twitchio.ext import commands

from emotes import GlobalEmotes
from errors import UserNotFoundError, UserChannelNotFoundError
from utils import BotActionUtils, UserUtils


class DefaultCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="shoutout", aliases=["so"])
    async def shoutout(self, ctx: commands.Context, target_user_name: str):
        if not await UserUtils.is_mod_author(ctx):
            return
        # Remove @ username prefix if present
        if target_user_name[0] == "@":
            target_user_name = target_user_name[1:] 
        # Get shoutout target
        try:
            user = await UserUtils.fetch_user(ctx, target_user_name)
            channel_info = await UserUtils.fetch_channel_info(ctx, user.id)
            
            announcement = (
                f"{GlobalEmotes.krey} {GlobalEmotes.krey} {GlobalEmotes.krey} "
                f"Go peep @{user.name} at https://twitch.tv/{user.name} "
                f"{GlobalEmotes.dog} {GlobalEmotes.dog} {GlobalEmotes.dog}"
            )
            if len(channel_info.game_name) != 0:
                announcement += f" last found enjoyin some {channel_info.game_name}!"
            else:
                announcement += "!"
            await BotActionUtils.make_announcement(self.bot, announcement)
        except (UserNotFoundError, UserChannelNotFoundError) as e:
            return
