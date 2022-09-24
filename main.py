import json
import os
from sys import stdout

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

# https://stackoverflow.com/a/234329


def walklevel(root_dir: str, level=1) -> tuple[str, list[str], list[str]]:
    """Walk through directories until a certain depth.
    Similiar to os.walk()

    Args:
        root_dir (str): Path to target directory
        level (int, optional): Depth. Defaults to 1.

    Yields:
        Iterator[tuple[str, list[str], list[str]]]: Root, directories, files
    """
    root_dir = root_dir.rstrip(os.path.sep)
    assert os.path.isdir(root_dir)
    num_sep = root_dir.count(os.path.sep)
    for root, dirs, files in os.walk(root_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def get_downloads_by_most_recent(download_path: str) -> list[str]:
    files: list[str] = []
    for root, dirnames, filenames in walklevel(download_path, 1):
        files.extend(
            map(lambda filename: os.path.join(root, filename), filenames))
    files.sort(key=os.path.getctime, reverse=True)
    return files


if __name__ == '__main__':
    config = get_config()
    downloads = get_downloads_by_most_recent(config["download_dir"])
    for file in downloads:
        print(file)
