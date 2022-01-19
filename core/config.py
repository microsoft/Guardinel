# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.utils.map import resources


class Config(ABC):
    """
    Abstract class for the config which is one of the inputs to the Concurrent Executor
    """
    __logger = resources.get('LOGGER')

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

    def logger(self):
        return self.__logger


class ConfigBuilder(ABC):

    """
    Abstract builder class which should be implemented by the wrappers to build the config
    """
    _name = 'ConfigBuilder'
    __logger = resources.get('LOGGER')

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
