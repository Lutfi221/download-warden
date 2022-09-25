import os
from sys import stdout
from config import get_config, get_user_variables
from explorer import get_current_explorer_path
from operators.Command import Command
from operators.Open import Open
from operators.Operator import Operator

from utils import print_latest_downloads, prompt_selection, walklevel

CONFIG_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'config.json')
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
    operators: list[Operator] = [Command(config), Open(config)]
    variables = get_user_variables(config['variables_json'])
    variables['e'] = get_current_explorer_path

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
