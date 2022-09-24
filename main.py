import json
import os
from sys import stdout

from utils import print_list, prompt_selection, walklevel

CONFIG_PATH = './config.json'
stdout.reconfigure(encoding='utf-8')


class Config:
    download_dir: str


def get_config() -> Config:
    """Reads config. Creates a default config file if doesn't exists.

    Returns:
        Config: Configuration
    """
    config_exists = os.path.isfile(CONFIG_PATH)
    if not config_exists:
        config: Config = {
            'download_dir': os.path.join(os.environ['USERPROFILE'], 'Downloads')
        }
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        return config

    with open(CONFIG_PATH, 'r') as f:
        config: Config = json.load(f)

    return config


def get_downloads_by_most_recent(download_path: str) -> list[str]:
    files: list[str] = []
    for root, dirnames, filenames in walklevel(download_path, 1):
        files.extend(
            map(lambda filename: os.path.join(root, filename), filenames))
    files.sort(key=os.path.getctime, reverse=True)
    return files


def main() -> None:
    config = get_config()
    downloads = get_downloads_by_most_recent(config['download_dir'])
    print_list(map(lambda filepath: filepath.split(
        os.sep)[-1], downloads), 'Most Recent:', 9)
    a = prompt_selection(['a', 'b', 'c', 'd'], 'testt:', True)
    print(a)


if __name__ == '__main__':
    main()
