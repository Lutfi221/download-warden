
import subprocess
from typing import Callable

from utils import expand_variables


def execute(cmd_string: str,
            variables: dict[str, str | Callable[[], str]]):
    exec_str = ' '.join(cmd_string.split(' ')[1:])
    exec_str = expand_variables(exec_str, variables)

    creationflags = subprocess.CREATE_NO_WINDOW
    with subprocess.Popen(exec_str,
                          shell=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          creationflags=creationflags) as p:
        print(p.stdout.read().decode())


execute.help_description = '''usage: execute [shell string]'''
