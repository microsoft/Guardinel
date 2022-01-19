# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import abstractmethod, ABC

from core.utils.map import resources


class Notifier(ABC):
    """
    Abstract notifier which should be implemented by all the notifiers in the system
    Concurrent Executor would invoke the notify method of the registered notifiers after the execution
    """
    __logger = resources.get('LOGGER')

    @abstractmethod
    def notify(self, entity, result):
        raise NotImplementedError()

    @abstractmethod
    def name(self):
        raise NotImplementedError()

    def logger(self):
        return self.__logger
