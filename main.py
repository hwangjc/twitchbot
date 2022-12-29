#!/usr/bin/env python3

from bot import Bot
from default_commands import DefaultCommands


def main():
    bot = Bot()

    bot.add_cog(DefaultCommands(bot))
    bot.init_user_commands()
    bot.run()

if __name__ == "__main__":
    main()
