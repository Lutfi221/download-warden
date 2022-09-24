
import json
import os
from typing import Callable


class Config(dict):
    download_dir: str
    variables_json: str


def get_config(config_path: str) -> Config:
    """Reads config. Creates a default config file if doesn't exists.

    Returns:
        Config: Configuration
    """
    config_exists = os.path.isfile(config_path)
    if not config_exists:
        config: Config = {
            'download_dir': os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            'variables_json': ''
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return config

    with open(config_path, 'r') as f:
        config: Config = json.load(f)

    return config


def get_user_variables(variables_json_path: str) -> dict[str, str | Callable[[], str]]:
    try:
        with open(variables_json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return {}
