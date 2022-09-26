
from genericpath import isfile
import os
import re
import shutil
from typing import Callable

from utils import expand_variables


def move_file(filepath: str, dest_dirpath: str):
    filename = os.path.basename(filepath)
    dest = os.path.join(dest_dirpath, filename)
    try:
        shutil.move(filepath, dest)
        print('{} -> {}'.format(filename, dest))
        return
    except Exception as e:
        print(e)
        print()


def move(cmd_string: str,
         variables: dict[str, str | Callable[[], str]]):
    args = cmd_string.split(' ')
    targets_str = args[1]
    dest_dirpath = ' '.join(args[2:])  # In case the path contains spaces
    dest_dirpath = expand_variables(dest_dirpath, variables)
    if os.path.isfile(dest_dirpath):
        dest_dirpath = os.path.dirname(dest_dirpath)

    # If it's "move 2" or "move 2,3,4"
    if re.match(r'\d+,?', targets_str):
        for number in targets_str.split(','):
            move_file(variables[number], dest_dirpath)
        return

    # If it's "move exe" or "move rar"
    extension = targets_str
    for i in range(0, 10):
        if variables[str(i)].endswith('.' + extension):
            move_file(variables[str(i)], dest_dirpath)
            return

    print('File not found')


move.help_description = '''usage: move [number] [destination]
   or: move [number, number, ...] [destination]
   or: move [extension] [destination]
      ex: move rar D:\\folder
'''
