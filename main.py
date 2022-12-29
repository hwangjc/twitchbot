#!/usr/bin/env python3

from bot import Bot

def main():
    bot = Bot()

    bot.init_user_commands()
    bot.run()

if __name__ == "__main__":
    main()
