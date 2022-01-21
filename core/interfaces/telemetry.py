# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from core.utils.map import resources


class Telemetry(ABC):
    """ Abstract class for all the telemetry implementations """

    __logger = resources.get('LOGGER')

    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def log(self, input_entity, tasks):
        raise NotImplementedError

    def console_logger(self):
        return self.__logger
