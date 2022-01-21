# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import getopt
import sys

from components.classes import instances_map
from components.utils.helper import pr_needs_block
from core.concurrent_executor import ConcurrentExecutor
from core.utils.helper import is_empty
from core.utils.map import resources
from dependency_injector import DependencyInjector

__logger = resources.get('LOGGER')
__tag = 'PolicyComplianceChecker'

# Usage examples:
# guardinel.py -p test_policy1 -p test_policy2 -o test_override1 -n terminal_notifier
# guardinel.py --policy test_policy1 --policy test_policy2 --notifier terminal_notifier --override test_override1


def parse_args(args_list):
    __entity = DependencyInjector.get(DependencyInjector.Constants.INPUT_ENTITY)
    __config_builder = DependencyInjector.get(DependencyInjector.Constants.CONFIG_BUILDER)

    __config_builder.with_instances_map(instances_map)

    try:
        # Options
        options = "vhjn:o:p:i:a:b:c:d:e:t:f:g:k:"

        # Long options
        long_options = ["verbose", "help", "disable_telemetry", "notifier=", "override=", "policy=", "pullrequest=",
                        "org=", "project=", "adoversion=", "user_key=", "user_id=", "type=", "approver_key=", "approver_user_id=", "telemetry="]

        # Parsing argument
        arguments, values = getopt.getopt(args_list, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                help_info()

            if currentArgument in ("-v", "--verbose"):
                resources.get('LOGGER').enable_debug()

            elif currentArgument in ("-n", "--notifier"):
                __logger.info(__tag, "Registering notifier : {}".format(currentValue))
                __config_builder.add_notifier(currentValue)

            elif currentArgument in ("-o", "--override"):
                __logger.info(__tag, "Registering override : {}".format(currentValue))
                __config_builder.add_global_override(currentValue)

            elif currentArgument in ("-p", "--policy"):
                __logger.info(__tag, "Registering policy/action : {}".format(currentValue))
                __config_builder.add_task(currentValue)

            elif currentArgument in ("-i", "--pullrequest"):
                __logger.info(__tag, "Input PR num : {}".format(currentValue))
                __entity.pr_num = currentValue

            elif currentArgument in ("-a", "--org"):
                __logger.info(__tag, "ADO Organisation : {}".format(currentValue))
                __entity.org = currentValue

            elif currentArgument in ("-b", "--project"):
                __logger.info(__tag, "ADO project : {}".format(currentValue))
                __entity.project = currentValue

            elif currentArgument in ("-c", "--adoversion"):
                __logger.info(__tag, "ADO API version : {}".format(currentValue))
                __entity.ado_version = currentValue

            elif currentArgument in ("-d", "--user_key"):
                __entity.pat = currentValue

            elif currentArgument in ("-e", "--user_id"):
                __entity.user_id = currentValue

            elif currentArgument in ("-t", "--type"):
                __entity.pipeline_type = currentValue

            elif currentArgument in ("-f", "--approver_key"):
                __entity.pr_approver_key = currentValue

            elif currentArgument in ("-g", "--approver_user_id"):
                __entity.pr_approver_user_id = currentValue

            elif currentArgument in ("-j", "--disable_telemetry"):
                __config_builder.telemetry_enabled = False

            elif currentArgument in ("-k", "--telemetry"):
                __config_builder.add_telemetry(currentValue)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    validate_entity(__entity)

    return __config_builder.build(), __entity


def validate_entity(__entity):
    """ validates the entity for the required attributes """
    if is_empty(__entity.pr_num):
        __logger.error(__tag, "PR num is missing!! Use the arg: '-i <pr_num>'")
        help_info()
        raise ValueError("PR num is missing!! Use the arg: '-i <pr_num>'")

    if is_empty(__entity.pat):
        __logger.error(__tag, "PAT is missing!! Use the arg: '-d <PAT>'")
        help_info()
        raise ValueError("PAT is missing!! Use the arg: '-d <PAT>'")

    if is_empty(__entity.pipeline_type) or __entity.pipeline_type not in ('android', 'ios', 'tmp', 'maglev'):
        __logger.error(__tag, "Invalid pipeline type!! Use the arg: '-t <android/ios>'")
        help_info()
        raise ValueError("Pipeline type is invalid!! Use the arg: '-t <android/ios>'")


def help_info():
    __logger.info(__tag,
                  "Please follow the below format for arguments:\n"
                  "arguments: -p/--policy : policy_identifier\n"
                  "           -o/--override : override_identifier\n"
                  "           -n/--notifier : notifier_identifier\n"
                  "           -i/--pullrequest : PullRequest id (required)"
                  "           -t/--type : android/ios (required)\n"
                  "           -v/--verbose : prints debug log\n"
                  "           -h/--help : print this info\n"

                  "           -a/--org : Azure DevOps Organisation \n"
                  "           -b/--project : Azure DevOps Project \n"
                  "           -c/--adoversion : Azure DevOps api_endpoint version \n"
                  "           -d/--user key : Azure devops User Key (required)\n"
                  "           -e/--user id : Azure devops User id (required)\n"
                  "           -f/--approver_key"
                  "           -g/--approver_user_id"
                  "           -j/--disable_telemetry (default: False)"
                  "           -k/--telemetry"
                  "Execution Steps:"
                  "-i PR number will be used to retrieve PR related metadata"
                  "-o overrides will be evaluated first. If any of them returns true, execution will be skipped"
                  "-p if execution is not skipped, policies will be executed in parallel"
                  "-n notifiers will be invoked with the results from policy executions"
                  "-a, -b, -c, -d, -e Azure Devops Parameters required to access the API endpoints"
                  "-f, -g User information Parameters required to approve PRs")


if __name__ == '__main__':
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    config, entity = parse_args(argumentList)

    executor = ConcurrentExecutor(config, entity)
    results = executor.start()
    __logger.debug(__tag, 'results: {}'.format(results))

    if pr_needs_block(results):
        exit(1)
