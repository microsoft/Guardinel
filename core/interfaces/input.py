# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.utils.map import resources


class InputEntity(ABC):
    """
    Abstract input entity class which the wrapper should implement to
    allow the other components to access the required values
    """
    __logger = resources.get('LOGGER')

    # custom data dict that can be used to store custom data from different policies to pass info across policies
    # and also to avoid redundant API calls
    custom_data = {}

    @abstractmethod
    def name(self):
        raise NotImplementedError()

    @abstractmethod
    def key(self):
        raise NotImplementedError()

    def logger(self):
        return self.__logger
