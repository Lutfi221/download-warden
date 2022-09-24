import json
import os

CONFIG_PATH = './config.json'


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


if __name__ == '__main__':
    config = get_config()
    print(config)
