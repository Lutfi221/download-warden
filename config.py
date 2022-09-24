
import json
import os


class Config:
    download_dir: str


def get_config(config_path: str) -> Config:
    """Reads config. Creates a default config file if doesn't exists.

    Returns:
        Config: Configuration
    """
    config_exists = os.path.isfile(config_path)
    if not config_exists:
        config: Config = {
            'download_dir': os.path.join(os.environ['USERPROFILE'], 'Downloads')
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return config

    with open(config_path, 'r') as f:
        config: Config = json.load(f)

    return config
