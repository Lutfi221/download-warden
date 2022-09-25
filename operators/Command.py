
import shlex
import subprocess
from typing import Callable
from operators.Operator import Operator
from utils import expand_variables, print_latest_downloads


class Command(Operator):
    name = 'Command'

    def call(self, downloads: list[str], variables: dict[str, Callable[[], str]]) -> None:
        self.variables = variables

        print_latest_downloads(downloads)

        while True:
            user_input = input(' > ')
            if user_input == 'exit':
                return
            cmd_string = expand_variables(user_input, self.variables)

            creationflags = subprocess.CREATE_NO_WINDOW

            if cmd_string[0] == '\t':
                creationflags = subprocess.CREATE_NEW_CONSOLE
                cmd_string = 'start cmd /K ' + shlex.quote(cmd_string[1:])

            with subprocess.Popen(cmd_string,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  creationflags=creationflags) as p:
                print(p.stdout.read().decode())
