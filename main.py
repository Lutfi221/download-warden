import os
from sys import stdout, argv
from config import get_config, get_user_variables
from explorer import get_current_explorer_path
from commands import process_cmd

from utils import get_downloads_by_most_recent

CONFIG_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'config.json')
stdout.reconfigure(encoding='utf-8')


def main() -> None:
    config = get_config(CONFIG_PATH)
    variables = get_user_variables(config['variables_json'])
    variables['root'] = config['download_dir']

    while True:
        variables['e'] = get_current_explorer_path
        downloads = get_downloads_by_most_recent(config['download_dir'])
        for i, downloadPath in enumerate(downloads):
            if (i > 9):
                break
            variables[str(i)] = downloadPath

        if len(argv) > 1:
            process_cmd(' '.join(argv[1:]), variables)
            return

        user_input = input('\n > ')
        process_cmd(user_input, variables)


if __name__ == '__main__':
    main()
