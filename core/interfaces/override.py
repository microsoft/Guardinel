# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.interfaces.config_entity import ConfigEntity
from core.utils.map import resources


class Override(ConfigEntity):
    """
    Abstract class that defines the basic methods to define an override
    Concurrent Executor would invoke the evaluate method to get the overrides' status
    """
    def __init__(self, config=None):
        super().__init__(config)

    @abstractmethod
    def evaluate(self, input_entity):
        raise NotImplementedError()

    def name(self):
        return self.__class__.__name__
