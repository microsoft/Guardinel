# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.interfaces.task import Task
from core.utils.constants import Constants


class HelloWorldPolicy(Task):

    def execute(self, input_entity):
        if input_entity.project == 'TestProject':
            return self.result(Constants.FAIL, message="Can't execute the policy on TestProject")

        return self.result(Constants.SUCCESS)

    def overrides(self):
        return ['approval_override']

    def name(self):
        return 'hello_world_policy'
