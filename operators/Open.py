
import os
import subprocess
from config import Config
from utils import expand_variables, print_latest_downloads, prompt_selection, truncate_list_of_downloads


class Open(Config):
    name = 'Open'

    def call(self, downloads: list[str], variables: dict[str]) -> None:

        while True:
            user_selection = prompt_selection(
                list(truncate_list_of_downloads(downloads[:9])), 'File to Open')
            try:
                subprocess.run('start "" "{}"'.format(
                    downloads[user_selection]), shell=True, check=True)
                return
            except Exception as e:
                print(e)
                print()
