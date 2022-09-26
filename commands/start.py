
import os
import re
import subprocess
from typing import Callable


def open_file(filepath: str, open_directory=False):
    if open_directory:
        path = os.path.dirname(filepath)
    else:
        path = filepath

    try:
        subprocess.run('start "" "{}"'.format(path), shell=True, check=True)
        return
    except Exception as e:
        print(e)
        print()


def start(cmd_string: str,
          variables: dict[str, str | Callable[[], str]]):
    args = cmd_string.split(' ')
    targets_str = args[-1]

    open_directory = args[1] == '-d'

    # If it's "open 2" or "open 2,3,4"
    if re.match(r'\d+,?', targets_str):
        for number in targets_str.split(','):
            open_file(variables[number], open_directory)
        return

    # If it's "open exe" or "open rar"
    extension = targets_str
    for i in range(0, 10):
        if variables[str(i)].endswith('.' + extension):
            open_file(variables[str(i)], open_directory)
            return

    print('File not found')


start.help_description = '''usage: open [-d] [number]
   or: open [-d] [number, number, ...]
   or: open [-d] [extension]
      ex: open rar

   Options:
      -d \tOpens the directory of the file
'''
