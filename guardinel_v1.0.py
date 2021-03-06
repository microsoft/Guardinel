# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import getopt
import json
import sys

from components.classes import instances_map
from components.pr_input_entity import PullRequestEntity
from components.utils.helper import pr_needs_block
from core.concurrent_executor import ConcurrentExecutor
from core.utils.helper import is_empty, get_value
from core.utils.map import resources
from dependency_injector import DependencyInjector

__logger = resources.get('LOGGER')
__tag = 'Guardinel'


class CmdlineInput:
    def __init__(self):
        self.config_path = None
        self.access_token = None


class Guardinel:

    default_config = 'guardinel.json'

    @staticmethod
    def start(_cmdline_input):
        with open(_cmdline_input.config_path, encoding='utf-8') as f:
            config_json = json.load(f)
            if get_value(config_json, ["log_level"], "").lower() == 'debug':
                resources.get('LOGGER').enable_debug()

            config, entity = Guardinel.build_config_entity(config_json, _cmdline_input.access_token)
            executor = ConcurrentExecutor(config, entity)
            return executor.start()

    @staticmethod
    def build_config_entity(config_file, access_token):
        config = Guardinel.build_config(config_file)
        entity = Guardinel.build_entity(get_value(config_file, ["input"]), access_token)
        return config, entity

    @staticmethod
    def build_entity(input_config, access_token):
        input_entity = PullRequestEntity()
        input_entity.pr_num = get_value(input_config, ["entity", "id"])
        input_entity.org = get_value(input_config, ["org"])
        input_entity.project = get_value(input_config, ["project"])
        input_entity.pat = access_token
        input_entity.ado_version = get_value(input_config, ["api", "version"])

        Guardinel.validate_entity(input_entity)
        return input_entity

    @staticmethod
    def build_config(config):
        __config_builder = DependencyInjector.get(DependencyInjector.Constants.CONFIG_BUILDER)
        __config_builder.with_instances_map(instances_map)

        for task in get_value(config, ["tasks"]):
            __config_builder.add_task(task)

        for task in get_value(config, ["notifiers"]):
            __config_builder.add_notifier(task)

        for override in get_value(config, ["global_overrides"]):
            __config_builder.add_global_override(override)

        for telemetry in get_value(config, ["telemetry"]):
            __config_builder.add_telemetry(telemetry)

        __config_builder.telemetry_enabled = get_value(config, ["telemetry_enabled"])

        return __config_builder.build()

    @staticmethod
    def validate_entity(input_entity):
        """ validates the entity for the required attributes """
        if is_empty(input_entity.pr_num):
            help_info()
            raise ValueError("PR num is missing in the config")

        if is_empty(input_entity.pat):
            help_info()
            raise ValueError("PAT is missing in the config")

        if is_empty(input_entity.ado_version):
            help_info()
            raise ValueError("ado_version is missing in the config")

        if is_empty(input_entity.org):
            help_info()
            raise ValueError("org is missing in the config")

        if is_empty(input_entity.project):
            help_info()
            raise ValueError("project is missing in the config")


def help_info():
    __logger.info(__tag,
                  "Please follow the below format for arguments:\n"
                  "arguments: -f/--config : path to config file\n"
                  "           -h/--help : print help\n"
                  "Refer this wiki for the config file format")


def parse_args(args_list, default):
    cmdline_in = CmdlineInput()
    cmdline_in.config_path = default
    cmdline_in.access_token = None

    # Options
    options = "hc:t:"

    # Long options
    long_options = ["help", "config=", "token="]

    # Parsing argument
    arguments, values = getopt.getopt(args_list, options, long_options)
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            help_info()

        elif currentArgument in ("-c", "--config"):
            cmdline_in.config_path = currentValue

        elif currentArgument in ("-t", "--token"):
            cmdline_in.access_token = currentValue

    return cmdline_in


if __name__ == '__main__':
    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]
    cmdline_input = parse_args(argumentList, default=Guardinel.default_config)
    results = Guardinel.start(cmdline_input)

    __logger.debug(__tag, 'results: {}'.format(results))

    if pr_needs_block(results):
        exit(1)
