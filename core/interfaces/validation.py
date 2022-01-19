# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.utils.map import resources


class Validation(ABC):
    """ Class to represent all Validations"""
    __logger = resources.get('LOGGER')

    def logger(self):
        return self.__logger

    @abstractmethod
    def validate(self, input_entity):
        raise NotImplementedError()
