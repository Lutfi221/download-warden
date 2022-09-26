
from typing import Callable
from commands.execute import execute
from commands.list_recent import list_recent
from commands.start import start

Variables = dict[str, str | Callable[[], str]]
CommandFunction = Callable[[str, list[str], Variables], str]


class CommandEntry():
    aliases: list[str]
    description: str
    help_description: str
    execute: CommandFunction

    def __init__(self, execute: CommandFunction, aliases: list[str],
                 description: str, help_description: str):
        self.execute = execute
        self.aliases = aliases
        self.description = description
        self.help_description = help_description

    def is_alias(self, alias: str) -> bool:
        return alias in self.aliases


REGISTERED_COMMANDS = [
    CommandEntry(start, ['open', 'start', 'o'],
                 'Opens a file(s)', start.help_description),
    CommandEntry(list_recent, ['list', 'l'],
                 'List recent downloads', list_recent.help_description),
    CommandEntry(execute, ['execute', 'x'],
                 'Execute shell string', execute.help_description)
]


def process_cmd(cmd_string: str, variables: Variables):
    splitted = cmd_string.split(' ')
    cmd_alias = splitted[0]

    for cmd_entry in REGISTERED_COMMANDS:
        if cmd_entry.is_alias(cmd_alias):

            # If asking for help
            if (len(splitted) == 2 and
                    (splitted[1].endswith('-help') or
                     splitted[1] == '-h')):
                print(cmd_entry.execute.help_description)
                return

            cmd_entry.execute(cmd_string, variables)
            return

    print("Unknown command '{}'".format(cmd_alias))
