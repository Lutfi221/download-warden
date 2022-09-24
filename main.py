import json
import os
from sys import stdout
from config import get_config
from operators.Command import Command
from operators.Operator import Operator

from utils import print_latest_downloads, prompt_selection, walklevel

CONFIG_PATH = './config.json'
stdout.reconfigure(encoding='utf-8')


def get_downloads_by_most_recent(download_path: str) -> list[str]:
    files: list[str] = []
    for root, dirnames, filenames in walklevel(download_path, 1):
        files.extend(
            map(lambda filename: os.path.join(root, filename), filenames))
    files.sort(key=os.path.getctime, reverse=True)
    return files


def main() -> None:
    config = get_config(CONFIG_PATH)
    operators: list[Operator] = [Command(config)]
    variables: dict[str, str] = {}

    while True:
        variables['root'] = config['download_dir']
        downloads = get_downloads_by_most_recent(config['download_dir'])

        for i, downloadPath in enumerate(downloads, 1):
            variables[str(i)] = downloadPath

        print_latest_downloads(downloads)

        op_index = prompt_selection(
            list(map(lambda op: op.name, operators)), 'Operators:', True)

        operators[op_index].call(downloads, variables)


if __name__ == '__main__':
    main()
