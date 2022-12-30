from typing import Callable

from twitchio.ext import commands
from twitchio import ChannelInfo, User

from errors import UserNotFoundError, UserChannelNotFoundError


class UserUtils:
    @staticmethod
    async def fetch_user(ctx: commands.Context, name: str) -> User:
        users = await ctx.bot.fetch_users(names=[name])
        if len(users) == 0:
            await ctx.send(f"Could not find user {name}")
            raise UserNotFoundError
        return users[0]

    @staticmethod
    async def fetch_channel_info(
        ctx: commands.Context, 
        user_id: str
    ) -> ChannelInfo:
        channel_infos = await ctx.bot.fetch_channels(broadcaster_ids=[user_id])     
        if len(channel_infos) == 0:
            raise UserChannelNotFoundError
        return channel_infos[0]


class BotActionUtils:
    @staticmethod
    async def make_announcement(bot: commands.Bot, message: str) -> None:
        # Check if the bot has the broadcaster_user property already set
        if not hasattr(bot, "broadcaster_user") or bot.broadcaster_user is None:
            broadcasters = await bot.fetch_users(names=[bot.broadcaster_name])
            setattr(
                bot, 
                "broadcaster_user", 
                bot.create_user(broadcasters[0].id, broadcasters[0].name)
            )
        await bot.broadcaster_user.chat_announcement(
            token=bot._connection._token,
            moderator_id=bot.user_id,
            message=message
        )


class CommandUtils:
    @staticmethod
    def mod_only_command(func: Callable) -> Callable:
        async def decorator(self, ctx: commands.Context, *args, **kwargs):
            if not ctx.author.is_mod:
                await ctx.reply("lol not a mod")
            else:
                await func(self, ctx, *args, **kwargs)
        return decorator

