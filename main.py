#!/usr/bin/env python3
import os

from bot import Bot
from cmds.default_commands import DefaultCommands
from cmds.generic_queue_commands import GenericQueueCommands


def main():
    # Initialize the persistent User Commands File
    cwd = os.path.abspath(os.path.dirname(__file__))

    persistent_rel_path = "./persistent/"
    persistent_abs_path = os.path.abspath(os.path.join(cwd, persistent_rel_path))
    if not os.path.isdir(persistent_abs_path):
        print(f"Making {persistent_abs_path}")
        os.mkdir(persistent_abs_path)

    ucf_rel_path = "./persistent/usercommands"
    ucf_abs_path = os.path.abspath(os.path.join(cwd, ucf_rel_path))
    if not os.path.isfile(ucf_abs_path):
        print(f"Making {ucf_abs_path}")
        open(ucf_abs_path, "w").close()

    bot = Bot(user_commands_file=ucf_abs_path)
    
    # init cogs / commands
    bot.add_cog(DefaultCommands(bot))
    bot.add_cog(GenericQueueCommands(bot))
    bot.init_user_commands()

    bot.run()

if __name__ == "__main__":
    main()
