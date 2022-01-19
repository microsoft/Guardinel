# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import traceback
from abc import ABC, abstractmethod

from core.exceptions import PolicyError
from core.utils.constants import Constants
from core.utils.helper import get_value
from core.utils.map import resources
from core.utils.metrics import MetricsData


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


class Validation(ABC):
    """ Class to represent all Validations in the SHIELD"""
    __logger = resources.get('LOGGER')

    def logger(self):
        return self.__logger

    @abstractmethod
    def validate(self, input_entity):
        raise NotImplementedError()


class Task(ABC):
    """
    Abstract entity that defines the task to be executed concurrently
    Concurrent Executor would invoke the execute method concurrently to run the task
    """
    __logger = resources.get('LOGGER')

    def __init__(self):
        self.metrics = MetricsData(self.name())

    @abstractmethod
    def execute(self, __input: InputEntity):
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


class Notifier(ABC):
    """
    Abstract notifier which should be implemented by all the notifiers in the system
    Concurrent Executor would invoke the notify method of the registered notifiers after the execution
    """
    __logger = resources.get('LOGGER')

    @abstractmethod
    def notify(self, entity, result):
        raise NotImplementedError()

    @abstractmethod
    def name(self):
        raise NotImplementedError()

    def logger(self):
        return self.__logger


class Action(Task, ABC):
    """
    Abstract class that defines the basic methods to define an action

    Action represents the tasks that SHIELD takes intuitively which improves the code/system/process.
    Action should never block the PR gate and it should only return one of the following values:
    NOTIFY/SUCCESS/FAIL - Post comments to the PR to inform the executed action.
    NO_ACTION - For some reasons, nothing got changed by the action. No notification will be sent to the PR/user

    Action can throw an exception for failures which will be marked for NOTIFY status

    """
    __logger = resources.get('LOGGER')
    __tag = 'Action Interface'

    def execute(self, __input: InputEntity):
        """
            This method will be invoked if the action is configured as a policy
        """
        try:
            action_result = self.execute_action(__input)

            # Ideally, implementations shouldn't return None but to be safe
            if action_result is None:
                return self.result(Constants.NO_ACTION)

            status = get_value(action_result, ['status'])
            if status not in self.accepted_statuses():
                self.__logger.warn(self.__tag, 'Updating status of {} from {} to {} to post comments in the PR!!'
                                   .format(self.name(), status, Constants.NOTIFY))
                action_result['status'] = Constants.NOTIFY

        except PolicyError as e:
            self.logger().error(self.__tag, traceback.format_exc())
            return self.result(Constants.NOTIFY, error=e)

        return action_result

    @abstractmethod
    def execute_action(self, input_entity, task_result=None):
        """ This method will be invoked if the action is added as a callback to a policy"""
        raise NotImplementedError()

    def name(self):
        return self.__class__.__name__

    def logger(self):
        return self.__logger

    @staticmethod
    def accepted_statuses():
        return [Constants.NOTIFY, Constants.NO_ACTION]


class Template(Task, ABC):
    """ Parent interface to identify templates """
    pass


class ActionTemplate(Action, ABC):
    """ Parent interface to identify action templates """
    pass
