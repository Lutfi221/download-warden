
from abc import abstractmethod

from config import Config


class Operator:
    name: str
    config: Config
    variables: dict[str, str] = {}

    @abstractmethod
    def __init__(self, config: Config):
        self.config = config
        return

    @abstractmethod
    def call(self, downloads: list[str], variables: dict[str]) -> None:
        pass
