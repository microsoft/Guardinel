# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from components.classes import instance_map
from core.interfaces.config import Config, ConfigBuilder
from core.utils.helper import get_values, is_empty


class PoliciesConfig(Config):

    """
    Config input to the concurrent executor. To be built based on the command line
    registrations of tasks, overrides and notifiers
    """

    policies = None
    notifiers = None
    policy_overrides = []
    shield_overrides = None
    telemetry_enabled = False
    telemetry = None

    def get_tasks(self):
        return self.policies

    def get_task_overrides(self):
        return self.policy_overrides

    def get_global_overrides(self):
        return self.shield_overrides

    def get_notifiers(self):
        return self.notifiers

    def get_telemetry(self):
        return self.telemetry

    def update_policy_overrides(self):
        """
        Returns list of overrides that tasks can be skipped for
        """
        _overrides = []
        for task in self.policies:
            _overrides.extend(task.overrides() or [])

        self.policy_overrides = get_values(self.instances_map, _overrides)


class PoliciesConfigBuilder(ConfigBuilder):

    """
    Config builder that validates the user input and builds the policies config
    """
    __name = 'PoliciesConfigBuilder'

    def __init__(self):
        super().__init__()
        self.__policies = []
        self.__notifiers = []
        self.__telemetry = self.default_telemetry()
        self.__policy_overrides = []
        self.__global_overrides = []
        self.telemetry_enabled = True

    def add_task(self, task):
        self.__policies.append(task)

    def add_global_override(self, override):
        self.__global_overrides.append(override)

    def add_notifier(self, notifier):
        self.__notifiers.append(notifier)

    def add_telemetry(self, telemetry):
        self.__telemetry.append(telemetry)

    def with_tasks(self, policies):
        self.__policies = policies
        return self

    def with_shield_overrides(self, overrides):
        return self.with_global_overrides(overrides)

    def with_global_overrides(self, overrides):
        self.__global_overrides = overrides
        return self

    def with_notifiers(self, notifiers):
        self.__notifiers = notifiers
        return self

    @staticmethod
    def default_telemetry():
        return []

    def build(self):
        """
        Parent class will make the base validation on the config
        Returns:

        """
        self.__validate()
        __config = PoliciesConfig(self.instances_map)
        __config.policies = get_values(self.instances_map, self.__policies)
        __config.update_policy_overrides()
        __config.notifiers = get_values(self.instances_map, self.__notifiers)
        __config.shield_overrides = get_values(self.instances_map, self.__global_overrides)
        __config.telemetry = get_values(self.instances_map, self.__telemetry)
        __config.telemetry_enabled = self.telemetry_enabled
        return __config

    def __validate(self):
        """
        This validates whether all the required components are configured. Otherwise,
        it will raise an exception on missing components
        """

        if is_empty(self.instances_map):
            raise ValueError('instances_map of components is not initiated! Please initiate it.')

        # warn if no notifiers are registered
        if self.__notifiers is None or len(self.__notifiers) == 0:
            self.logger().warn(self._name, 'No notifiers are set!!')

        # raise exception if there are no policies registered
        if self.__policies is None or len(self.__policies) == 0:
            raise ValueError('Tasks are not set! Cannot build config!')
