# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    """
    Abstract base class for all the logger implementations of this tool
    """

    __debug = False

    @abstractmethod
    def info(self, tag, message):
        raise NotImplementedError

    @abstractmethod
    def error(self, tag, message):
        raise NotImplementedError

    @abstractmethod
    def debug(self, tag, message):
        raise NotImplementedError

    @abstractmethod
    def warn(self, tag, message):
        raise NotImplementedError

    def enable_debug(self):
        self.__debug = True

    def debug_enabled(self):
        return self.__debug

