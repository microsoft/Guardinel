# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import traceback
from abc import abstractmethod, ABC

from core.utils.constants import Constants
from core.exceptions import PolicyError
from core.interfaces.task import Task
from core.utils.helper import get_value
from core.utils.map import resources


class Action(Task, ABC):
    """
    Abstract class that defines the basic methods to define an action

    Action represents the tasks that Guardinel takes intuitively which improves the code/system/process.
    Action should never block the PR gate and it should only return one of the following values:
    NOTIFY/SUCCESS/FAIL - Post comments to the PR to inform the executed action.
    NO_ACTION - For some reasons, nothing got changed by the action. No notification will be sent to the PR/user

    Action can throw an exception for failures which will be marked for NOTIFY status

    """
    __logger = resources.get('LOGGER')
    __tag = 'Action Interface'

    def execute(self, input_entity):
        """
            This method will be invoked if the action is configured as a policy
        """
        try:
            action_result = self.execute_action(input_entity)

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


class ActionTemplate(Action, ABC):
    """ Parent interface to identify action templates """
    pass
