
from typing import Callable


def quit(cmd_string: str,
         variables: dict[str, str | Callable[[], str]]):
    exit()


quit.help_description = '''usage: exit'''
