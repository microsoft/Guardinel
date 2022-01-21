# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.utils.constants import Constants
from core.utils.map import resources

__logger = resources.get('LOGGER')
__tag = 'ComponentsHelper'


def pr_needs_block(policy_results):
    """
        Returns true if any of the results is FAIL or API_CALL_ERROR
                false if there are no failed policies or if the PR is a fix for one or more policy fails
    """
    if policy_results is None:
        return True

    block_pr = False
    for result in policy_results:
        if result is None or 'status' not in result:
            raise RuntimeError('Invalid result: {}'.format(result))

        if result['status'] in [Constants.FAIL, Constants.API_CALL_ERROR]:
            # log all the failed policies with their error messages
            __logger.error(__tag, '{} failed with error: {}'.format(result['name'], result['error']))
            block_pr = True
        if result['status'] == Constants.ALLOW_MERGE:
            # if the PR is fix for any of the policies, allow the PR to merge regardless of any fails
            __logger.info(__tag, '{} is being fixed by this PR'.format(result['name']))
            return False

    return block_pr
