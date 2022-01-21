# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import abstractmethod, ABC

from core.utils.constants import Constants
from core.utils.map import resources
from core.utils.metrics import MetricsData


class Task(ABC):
    """
    Abstract entity that defines the task to be executed concurrently
    Concurrent Executor would invoke the execute method concurrently to run the task
    """
    __logger = resources.get('LOGGER')

    def __init__(self):
        self.metrics = MetricsData(self.name())

    @abstractmethod
    def execute(self, input_entity):
        raise NotImplementedError()

    @abstractmethod
    def overrides(self):
        raise NotImplementedError()

    def callbacks(self):
        """
        List of callbacks that needs to be executed after a task is executed.
        Callbacks should implement the interface core.interfaces.Action
        """
        return []

    @abstractmethod
    def name(self):
        raise NotImplementedError()

    def get_overriders(self, override_evals: map):
        __overriders = []
        for override in self.overrides() or []:
            if override_evals.get(override):
                __overriders.append(override)
        self.__logger.info(self.name(), 'Applied overrides: {} and Succeeded Overrides: {}'
                           .format(self.overrides(), __overriders))
        return __overriders

    def logger(self):
        return self.__logger

    def set_metrics(self, metrics):
        self.metrics = metrics

    def result(self, status, overridden_by=None, message='', error=None):
        """
        All the concrete tasks are expected to return result in this format

        Args:
            status: defines the status of the task execution. Possible values are in SUCCESS/FAIL/OVERRIDDEN
            overridden_by: defines the override_identifier in case of overridden task
            message: provides error message in case the task fails
            error: PolicyError object with fail info in case of fail status

        Returns: standard json format for the result

        """
        if status == Constants.OVERRIDDEN:
            message += ' Overridden by {}'.format(overridden_by)

        return {
            'name': self.name(),
            'overrides': self.overrides(),
            'overridden_by': overridden_by,
            'status': status,
            'message': message,
            'exception': error.__class__.__name__ if error else '',
            'error': error.__dict__ if error else ''
        }


class TaskTemplate(Task, ABC):
    """ Parent interface to identify task templates """
    pass
