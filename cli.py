# cli.py
# Interactive implementation based off bot.py that runs locally in shell, written specifically for someone.
# On first run: python -m cli init username
# Consequent runs: python -m cli

__version__ = "1.1.0"

import sys
import cmd
import argparse

from planning import *
from planning import list_users

user_data = None

class PlanningShell(cmd.Cmd):
    intro = f"Type help or ? to list commands."
    prompt = "\n> "

    def do_add(self, arg):
        """Add <date> to database.
<date> format: day/month/year or day-month-year
<date> can also be "today" or "yesterday" """
        pass

    def do_remove(self, arg):
        """Remove previous date entry."""
        pass

    def do_predict(self, arg):
        """Calculate and output prediction."""
        pass

    def do_view(self, arg):
        """Pretty print and list entries."""
        pass

    def do_save(self, arg):
        """Save changes to database."""
        pass

    def do_exit(self, arg):
        """Say bye."""
        print("Bye.")
        return True
    

def parse_arguments():
    """Parses command line arguments and returns them."""

    parser = argparse.ArgumentParser(description="period tracker")

    subparsers = parser.add_subparsers()

    init_subparser = subparsers.add_parser("init", help="setup user profile and data")
    init_subparser.add_argument("user", type=str, help="user id") 

    # draft: lazy to implement
    #run_subparser = subparsers.add_parser("run", help="launch interactive session")
    #run_subparser.add_argument("user", type=str, help="user id")

    parser.add_argument(
        "--version",
        action="version",
        version=f"{__version__}",
        help="show version number and exit"
    )

    return parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        # use first user profile
        user_data = UserData(list_users()[0])
        PlanningShell().cmdloop()
    else:
        # assumes there is only one positional argument to handle: init
        # flawed implementation ik
        setup()

        args = parse_arguments()

        if adduser(args.user):
            print(f'User "{args.user}" added.')
        else:
            print(f'User "{args.user}" already exists.')