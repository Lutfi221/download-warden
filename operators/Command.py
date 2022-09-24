
import os
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
            os.popen(cmd_string)
