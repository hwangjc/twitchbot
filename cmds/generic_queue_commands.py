from typing import Callable

from twitchio.ext import commands

from custom_queue import Queue, QueueItem
from emotes import GlobalEmotes
from errors import QueueItemDNEError, QueueItemNotUniqueError
from utils import CommandUtils


def check_queue_open(func: Callable) -> Callable:
    async def decorator(self, ctx: commands.Context, *args, **kwargs):
        if not (
            hasattr(self.bot, "generic_queue") and 
            self.bot.generic_queue.is_open
        ):
            await ctx.reply(f"{GlobalEmotes.rlytho} queue isn't even open...") 
        else:
            await func(self, ctx, *args, **kwargs)
    return decorator


class GenericQueueCommands(commands.Cog):
    """
    Generic queue management / interaction commands.

    Commands:
        - open: open the queue
        - close: close the queue
        - clear: clear the queue
        - next: get next item in queue
        - join: author request to join queue
        - leave: author request to leave queue
        - queue: list items in the queue
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.command(name="open")
    @CommandUtils.mod_only_command
    async def queue_open(self, ctx: commands.Context):
        # Check to see if 'queue' already exists
        if not hasattr(self.bot, "generic_queue"):
            # Generic queue defaults to unique queue
            setattr(self.bot, "generic_queue", Queue(is_unique=True))
        # Open queue
        if not self.bot.generic_queue.is_open:
            self.bot.generic_queue.open()
            await ctx.send(
                f"Queue is open {GlobalEmotes.krey} join the queue with !join, "
                "leave with !leave"
            )
        else:
            await ctx.send(f"{GlobalEmotes.cmonbruh} queue is already open...")

    @commands.command(name="close")
    @CommandUtils.mod_only_command
    @check_queue_open
    async def queue_close(self, ctx: commands.Context):
        self.bot.generic_queue.close()
        await ctx.send(f"Queue is now closed {GlobalEmotes.notlikethis}")

    @commands.command(name="clear")
    @CommandUtils.mod_only_command
    @check_queue_open
    async def queue_clear(self, ctx: commands.Context):
        self.bot.generic_queue.clear()
        await ctx.send(f"Queue has been cleared {GlobalEmotes.tea}")

    @commands.command(name="next")
    @CommandUtils.mod_only_command
    @check_queue_open
    async def queue_next(self, ctx: commands.Context):
        item = self.bot.generic_queue.next()
        if item is None:
            await ctx.send(f"Oops looks like the queue is empty")
            return
        await ctx.send(f"@{item.id} {item.data}") 

    @commands.command(name="join")
    @check_queue_open
    async def queue_join(self, ctx: commands.Context, *args):
        # Use the authors twitch name as the id in the queue
        item_id = ctx.author.name
        item_data = " ".join(args)

        try:
            self.bot.generic_queue.join(
                QueueItem(id=item_id, data=item_data)            
            )
        except QueueItemNotUniqueError as e:
            await ctx.reply("you're already in the queue...")
            return
        await ctx.reply("you're in")

    @commands.command(name="leave")
    @check_queue_open
    async def queue_leave(self, ctx: commands.Context):
        item_id = ctx.author.name
        try:
            self.bot.generic_queue.leave(item_id)
        except QueueItemDNEError as e:
            await ctx.reply("you're not even in the queue...")
            return
        await ctx.reply("peace")

    @commands.command(name="queue")
    @check_queue_open
    async def queue_list(self, ctx: commands.Context):
        items = self.bot.generic_queue.list()
        if len(items) == 0:
            await ctx.send("Queue is currently empty :O") 
            return
        message = "Current queue: "
        for i in range(len(items)):
            message += f"{i+1}. {items[i].id} "
        await ctx.send(message)


