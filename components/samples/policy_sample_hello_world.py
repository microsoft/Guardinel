from core.interfaces.task import Task
from core.utils.constants import Constants


class HelloWorldPolicy(Task):
    def execute(self, input_entity):
        return self.result(Constants.SUCCESS)

    def overrides(self):
        return []

    def name(self):
        return 'hello_world_policy'
