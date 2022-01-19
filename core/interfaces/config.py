# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.utils.helper import is_empty
from core.utils.map import resources


class Config(ABC):
    """
    Abstract class for the config which is one of the inputs to the Concurrent Executor
    """
    __logger = resources.get('LOGGER')

    def __init__(self):
        self.__class_map = None

    @abstractmethod
    def get_tasks(self):
        raise NotImplementedError()

    @abstractmethod
    def get_task_overrides(self):
        raise NotImplementedError()

    @abstractmethod
    def get_global_overrides(self):
        raise NotImplementedError()

    @abstractmethod
    def get_notifiers(self):
        raise NotImplementedError()

    def get_instances(self, names: list):
        """
        Returns a list of instances identifies by the given names
        """
        if is_empty(self.__class_map):
            raise

        instances = []
        for name in names:
            inst = self.__class_map.get(name)
            if inst is None:
                err = 'module {} not found in class_map! Check spelling! ' \
                      'If new entity, please add an entry in the class_map'.format(name)
                raise ModuleNotFoundError(err)
            instances.append(inst)

        return instances

    def logger(self):
        return self.__logger


class ConfigBuilder(ABC):
    """
    Abstract builder class which should be implemented by the wrappers to build the config
    """
    _name = 'ConfigBuilder'
    __logger = resources.get('LOGGER')

    def __init__(self):
        self.__class_map = None

    def with_class_map(self, class_map):
        self.__class_map = class_map
        return self

    @abstractmethod
    def with_tasks(self, tasks):
        raise NotImplementedError()

    @abstractmethod
    def with_global_overrides(self, overrides):
        raise NotImplementedError()

    @abstractmethod
    def with_notifiers(self, notifiers):
        raise NotImplementedError()

    @abstractmethod
    def build(self) -> Config:
        raise NotImplementedError()

    def logger(self):
        return self.__logger
