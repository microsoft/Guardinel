# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.interfaces.override import Override


class ApprovalOverride(Override):

    def evaluate(self, input_entity):
        if input_entity.is_approved_by(self.get_approvers()):
            return True

        return False

    def name(self):
        return 'approval_override'

    @staticmethod
    def get_approvers():
        return ['testapprover1@testmail.com', 'testapprover2@testmail.com']
