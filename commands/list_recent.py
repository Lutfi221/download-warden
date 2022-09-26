
import os
from typing import Callable


def list_recent(cmd_string: str,
                variables: dict[str, str | Callable[[], str]]):
    for i in range(0, 10):
        print('{}. {}'.format(i, os.path.basename(variables[str(i)])))


list_recent.help_description = '''usage: list'''
