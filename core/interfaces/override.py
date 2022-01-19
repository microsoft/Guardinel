# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.utils.map import resources


class Override(ABC):
    """
    Abstract class that defines the basic methods to define an override
    Concurrent Executor would invoke the evaluate method to get the overrides' status
    """
    __logger = resources.get('LOGGER')

    @abstractmethod
    def evaluate(self, input_entity):
        raise NotImplementedError()

    @abstractmethod
    def name(self):
        return self.__class__.__name__

    def logger(self):
        return self.__logger
