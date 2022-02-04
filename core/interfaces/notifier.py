# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from abc import abstractmethod

from core.interfaces.config_entity import ConfigEntity


class Notifier(ConfigEntity):
    """
    Abstract notifier which should be implemented by all the notifiers in the system
    Concurrent Executor would invoke the notify method of the registered notifiers after the execution
    """
    @abstractmethod
    def notify(self, entity, result):
        raise NotImplementedError()
