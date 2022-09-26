
import re
import subprocess
from typing import Callable


def open_file(path: str):
    try:
        subprocess.run('start "" "{}"'.format(path), shell=True, check=True)
        return
    except Exception as e:
        print(e)
        print()


def start(cmd_string: str,
          variables: dict[str, str | Callable[[], str]]):
    args = cmd_string.split(' ')
    targets_str = args[1]

    # If it's "open 2" or "open 2,3,4"
    if re.match(r'\d+,?', targets_str):
        for number in targets_str.split(','):
            open_file(variables[number])
        return

    # If it's "open exe" or "open rar"
    extension = targets_str
    for i in range(0, 10):
        if variables[str(i)].endswith('.' + extension):
            open_file(variables[str(i)])
            return

    print('File not found')


start.help_description = '''usage: open [number]
   or: open [number, number, ...]
   or: open [extension]
     ex: open rar'''
