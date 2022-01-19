# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

class Constants:
    """
    Provides the constants that will be used across the system for marking the status
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
