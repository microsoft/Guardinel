# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.exceptions import APICallFailedError


class FailedToAddReviewerError(APICallFailedError):
    def __init__(self, reviewer):
        super().__init__()
        self.message = 'Attempt to add {} to the PR failed'.format(reviewer)
        self.suggestion = 'Please get this PR approved from {}'.format(reviewer)


class FailedToAttachWorkItemError(APICallFailedError):
    def __init__(self, work_item_id):
        super().__init__()
        self.message = 'Attempt to attach the work item {} to the PR failed'.format(work_item_id)
        self.suggestion = 'Please attach the work item {} to this PR to close this comment'.format(work_item_id)


class FailedToUpdateFieldsError(APICallFailedError):
    def __init__(self, work_item_id, field_payload):
        super().__init__()
        self.message = 'Failed to update field values in the work item: {}'.format(work_item_id)
        self.suggestion = 'Please update the fields {} in the work item: {}'.format(field_payload, work_item_id)
