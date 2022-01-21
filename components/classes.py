# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from components.samples.notifier_sample_sysout_notifier import CommandLineNotifier
from components.samples.override_sample_approver_override import ApprovalOverride
from components.samples.policy_sample_hello_world import HelloWorldPolicy

instances_map = {
    # policies
    'hello_world_policy': HelloWorldPolicy(),

    # overrides
    'approval_override': ApprovalOverride(),

    # notifiers
    'cmdline_notifier': CommandLineNotifier()

}
