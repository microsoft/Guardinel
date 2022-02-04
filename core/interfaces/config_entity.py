from abc import ABC

from core.utils.helper import is_empty
from core.utils.map import resources


class ConfigEntity(ABC):

    __logger = resources.get('LOGGER')

    def __init__(self, config=None):
        self.config = config

    def config_get(self, key):
        if is_empty(self.config):
            return None
        return self.config.get(key)

    def name(self):
        return self.__class__.__name__

    def logger(self):
        return self.__logger
