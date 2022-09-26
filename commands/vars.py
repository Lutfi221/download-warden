
from typing import Callable


def vars(cmd_string: str,
         variables: dict[str, str | Callable[[], str]]):
    for key in variables:
        if callable(variables[key]):
            value = variables[key]()
        else:
            value = variables[key]
        print('${}:\t{}'.format(key, value))


vars.help_description = '''usage: vars'''
