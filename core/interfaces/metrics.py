# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import abstractmethod, ABC


class Metrics(ABC):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def value(self):
        return self.data

    @abstractmethod
    def append(self, value):
        raise NotImplementedError
