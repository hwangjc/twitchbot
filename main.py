#!/usr/bin/env python3

from bot import Bot
from cmds.default_commands import DefaultCommands
from cmds.queue_commands import QueueCommands


def main():
    bot = Bot()
    
    # init cogs / commands
    bot.add_cog(DefaultCommands(bot))
    bot.add_cog(QueueCommands(bot))
    bot.init_user_commands()

    bot.run()

if __name__ == "__main__":
    main()
