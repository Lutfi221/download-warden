
import os
from config import Config
from operators.Operator import Operator
from utils import expand_variables, print_latest_downloads


class Command(Operator):
    name = 'Command'

    def call(self, downloads: list[str], variables: dict[str]) -> None:
        self.variables = variables
            
        print_latest_downloads(downloads)

        while True:
            user_input = input(' > ')
            if user_input == 'exit':
                return
            cmd_string = expand_variables(user_input, self.variables)
            print(os.popen(cmd_string).read())
