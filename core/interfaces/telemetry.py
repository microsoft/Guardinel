# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.interfaces.config_entity import ConfigEntity


class Telemetry(ConfigEntity):
    """ Abstract class for all the telemetry implementations """

    @abstractmethod
    def log(self, input_entity, tasks):
        raise NotImplementedError
