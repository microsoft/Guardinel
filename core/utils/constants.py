# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

class Constants:
    """
    Provides the constants that will be used across the system
    """
    # ------ Task Status Constants ------ #
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    # Result flag that marks a policy which was overridden by any of its overrides
    OVERRIDDEN = 'OVERRIDDEN'
    # Result flag that identifies if the current PR is a fix for any of the policy breaches
    ALLOW_MERGE = 'ALLOW_MERGE'
    # Flag that marks that the result is to be informed to the committer.
    # Gate will pass always.
    NOTIFY = 'NOTIFY'
    # Flag that marks that no action was taken as part of the SHIELD ACTION execution
    # Gate will pass always.
    NO_ACTION = 'NO_ACTION'
    # Flag that marks an API call error in the policy/action.
    # Gate will fail and users should rerun after sometime
    API_CALL_ERROR = 'API_CALL_ERROR'
    # Flag that marks an unexpected error in the policy.
    # Gate will pass still to allow users to merge their changes
    UNEXPECTED_ERROR = 'UNEXPECTED_ERROR'

    # ------ Work Item Tag Constants ------ #
    # Tag to add work items which were cloned by SHIELD
    SHIELD_CLONED_TAG = 'shield_cloned'

    # ------ Ring Blocker values in Work Items ------ #
    RING_0 = '0 - Canary'
    RING_0s = '0s - SlimCore'
    RING_1 = '1 - Microsoft Teams'
    RING_1_5 = '1.5 - TAP IT'
    RING_2 = '2 - Microsoft'
    RING_3 = '3 - TAP'
    RING_3_6 = '3.6 - Public Preview'
    RING_4 = '4 - World'

    # ------ Other Constants ------ #
    FIELD_NOT_FOUND = 'FIELD_NOT_FOUND'
