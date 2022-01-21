# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from components.samples.override_sample_approver_override import ApprovalOverride
from components.samples.policy_sample_hello_world import HelloWorldPolicy

instances_map = {
    # policies
    'hello_world_policy': HelloWorldPolicy(),

    # overrides
    'approval_override': ApprovalOverride()

}
