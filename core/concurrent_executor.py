# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import threading
import traceback
from concurrent import futures
from datetime import datetime

from core.exceptions import GuardinelError, APICallFailedError
from core.utils.constants import Constants
from core.utils.helper import is_empty
from core.utils.map import resources


class ConcurrentExecutor:
    """
    Executor that takes care of executing the submitted tasks concurrently.
    It majorly relies on the two things:
        config - which defines the tasks, overrides and notifiers
        input_entity - entity which tasks would be validating

    Steps:
    When started, the executor would
    - evaluate all the registered overrides
    - invoke all the registered tasks
    - skip the tasks that are overridden
    - return list of results for all the tasks
    """

    __logger = resources.get('LOGGER')
    __name = 'ConcurrentExecutor'

    def __init__(self, config, input_entity, thread_count=3):
        super().__init__()
        self.config = config
        self.input_entity = input_entity
        self.thread_count = thread_count
        self.overrides_map = {}

    def evaluate_overrides(self, overrides_list):
        """
        Returns: map of override_identifier mapped to its evaluated values
        """
        result_map = {}
        if overrides_list is not None:
            for override in overrides_list:
                override_name = override.name()
                if not self.overrides_map.get(override_name):
                    self.overrides_map[override_name] = override.evaluate(self.input_entity)
                result_map[override_name] = self.overrides_map.get(override_name)
        return result_map

    def exec_task_and_callbacks(self, task):
        task.metrics.update_basic_fields(self.input_entity)
        task_result = self.exec_task(task)
        # callbacks tied to the task will be executed
        self.exec_callback(task, task_result)
        task.metrics.append(task_result)
        return task_result

    def exec_task(self, task):
        """
        Method that thread would invoke on a task.
        Task would be skipped if any of its override is set to True

        Args:
            task: task to be executed

        Returns: result json

        """
        __o_riders = task.get_overriders(self.overrides_map)
        if len(__o_riders) > 0:
            self.__logger.info(self.__name, '{} is skipped by {}'.format(
                task.name(), __o_riders))
            return task.result(Constants.OVERRIDDEN, __o_riders)

        self.__logger.debug(self.__name, "%s processing %s" % (
            threading.current_thread().name, task.name()))
        self.__logger.info(self.__name, 'Task Execution start: {} for pr {}...'.format(
            task.__class__.__name__, self.input_entity.key()))

        try:
            result = task.execute(self.input_entity)

        except APICallFailedError as e:
            self.__logger.error(self.__name, "API call error while executing the action {}: {}"
                                .format(task.name(), e))
            self.__logger.error(self.__name, traceback.format_exc())
            result = task.result(Constants.API_CALL_ERROR, error=e)
        except GuardinelError as e:
            self.__logger.error(self.__name, "Unhandled policy error while executing the action {}: {}"
                                .format(task.name(), e))
            self.__logger.error(self.__name, traceback.format_exc())
            result = task.result(Constants.FAIL, error=e)
        except Exception as e:
            self.__logger.error(self.__name, "Unexpected error while executing the task {}: {}"
                                .format(task.name(), e))
            self.__logger.error(self.__name, traceback.format_exc())
            result = task.result(Constants.UNEXPECTED_ERROR, error=e)

        self.__logger.info(self.__name, 'Task Execution complete: {}. Result: {}'.format(
            task.__class__.__name__, result))

        return result

    def exec_callback(self, task, task_result):
        if is_empty(task.callbacks()):
            return

        # if the task is overridden, don't execute callbacks as well
        __o_riders = task.get_overriders(self.overrides_map)
        if len(__o_riders) > 0:
            self.__logger.info(self.__name, "Also, skipped the execution of the callbacks of '{}' for the "
                                            "overrides '{}'".format(task.name(), __o_riders))
            return

        callback_results = {}
        for callback in self.config.get_instances(task.callbacks()):
            self.__logger.info(self.__name, '[{}] Executing the action {} on result {}'
                               .format(task.name(), callback.name(), task_result))
            try:
                callback.set_metrics(task.metrics.sub_metrics(callback.name()))
                callback_result = callback.execute_action(self.input_entity, task_result)
                callback_results[callback.name()] = callback_result
                callback.metrics.append(callback_result)
            except Exception as e:
                self.__logger.warn(self.__name, traceback.format_exc())
                callback_results[callback.name()] = 'Callback failed with error: {}'.format(e)
                callback.metrics.add('status', Constants.UNEXPECTED_ERROR)
                callback.metrics.add('exception', e.__class__.__name__)
                callback.metrics.add('error', traceback.format_exc())
        task_result['callback_results'] = callback_results

    def start(self):
        """
        Initializes the thread workers and submits the registered tasks from config.
        After the execution of all the tasks, notifiers would be invoked with the result set

        Returns:
        Once execution of all the tasks is completed, returns a list of all the results in
        a standard json format
        """
        if self.config is None:
            raise ModuleNotFoundError('config object is missing!!')

        global_overrides = self.evaluate_overrides(self.config.get_global_overrides())
        if any(global_overrides.values()):
            self.__logger.info(self.__name, "Global overrides {} evaluated to true. Skipping the execution!!"
                               .format(global_overrides))
            return []

        self.__logger.info(self.__name, "Initializing ConcurrentExecutor...")
        self.evaluate_overrides(self.config.get_task_overrides())
        ex = futures.ThreadPoolExecutor(max_workers=self.thread_count)
        results = ex.map(self.exec_task_and_callbacks, self.config.get_tasks())
        self.__logger.info(self.__name, "Exiting ConcurrentExecutor...")
        ex.shutdown()
        normalised_results = list(results)

        self.notify(normalised_results)

        if self.config.telemetry_enabled:
            self.send_metrics()
        return normalised_results

    def notify(self, results):
        """
        Notify the results with the registered notifiers

        Args:
            results: collection of results from all the tasks execution
        """
        if results is None or self.config.get_notifiers() is None or len(self.config.get_notifiers()) == 0:
            return

        for notifier in self.config.get_notifiers():
            self.__logger.info(self.__name, 'invoking notifier {}'.format(notifier.name()))
            notifier.notify(self.input_entity, results)

    def send_metrics(self):
        if not self.config.get_telemetry():
            return

        for telemetry in self.config.get_telemetry():
            self.__logger.info(self.__name, 'invoking telemetry: {}'.format(telemetry.name()))
            try:
                start_time = datetime.now()
                telemetry.log(self.input_entity, self.config.get_tasks())
                time_delta = datetime.now() - start_time
                self.__logger.info(self.__name, '{} took {} seconds to complete!'.
                                   format(telemetry.name(), time_delta.total_seconds()))
            except Exception as e:
                self.__logger.error(self.__name, traceback.format_exc())
                self.__logger.error(self.__name, 'Skipping error that occurred while invoking telemetry {}: Error: {}'
                                    .format(telemetry.name(), e))
