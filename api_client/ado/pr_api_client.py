# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json

from api_client.exceptions import FailedToAddReviewerError
from core.api.caller import get, put
from api_client.ado.endpoints import endpoint_map
from core.api.interfaces.pr_api_client import PullRequestApiClientInterface
from core.utils.map import resources


class PullRequestClient(PullRequestApiClientInterface):
    __logger = resources.get('LOGGER')
    __name = 'PullRequestClient'

    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.endpoint = endpoint_map['pr_by_id'].format(entity.org, entity.project, entity.pr_num, entity.ado_version)
        self.__data = None
        self.__comment_threads = None
        self.parent_ids = None
        self.changed_lines = []
        self.__changed_files_info = []

    def data(self):
        if self.__data is None:
            self.__logger.info(self.__name, 'Fetching Pull-Request metadata for PR {}...'.format(self.entity.pr_num))
            self.__data = get(self.endpoint, self.entity.pat)
        return self.__data

    def get_creator(self):
        return self.data()['createdBy']

    def get_creator_alias(self):
        return self.data()['createdBy']['uniqueName']

    def get_work_items(self):
        """ Retrieves the work-items tied to the pull request """
        return self.entity.linked_work_items()

    def get_comment_threads(self):
        if self.__comment_threads is None:
            entity = self.entity
            self.__logger.info(self.__name, "Fetching Pull-Request comment threads for PR {}...".format(entity.pr_num))
            endpoint = endpoint_map['pr_comments'].format(entity.org, entity.project, entity.repo(), entity.pr_num)
            self.__comment_threads = get(endpoint, entity.pat)
        return self.__comment_threads

    def get_commits(self):
        endpoint = endpoint_map['pr_commits'].format(self.entity.org,
                                                     self.entity.project,
                                                     self.entity.repo(),
                                                     self.entity.pr_num,
                                                     self.entity.ado_version)
        resp = get(endpoint, self.entity.pat)
        return resp

    @staticmethod
    def get_diff(_entity):
        """
        Returns the files modified in the given entity
        """
        endpoint = endpoint_map['ado_diff_by_commit'].format(_entity.org, _entity.project, _entity.repo())
        params = {
            "baseVersion": _entity.target_branch().replace('refs/heads/', ''),  # develop branch
            "baseVersionType": "branch",
            "targetVersion": _entity.source_branch().replace('refs/heads/', ''),  # dev's private branch
            "targetVersionType": "branch",
            "api-version": _entity.ado_version
        }
        resp = get(endpoint, _entity.pat, params)
        return resp

    def changes(self, repo_id, commit_id):
        if self.parent_ids is None:
            entity = self.entity
            endpoint = endpoint_map['commit'].format(entity.org, entity.project, repo_id, commit_id, entity.ado_version)
            json_obj = get(endpoint, entity.pat)
            self.parent_ids = json_obj['parents']
        self.__logger.debug(self.__name, self.parent_ids)
        return self.parent_ids

    def get_file_add_diff(self, diff_parameters, repo_id):
        if not self.changed_lines:
            entity = self.entity
            endpoint = endpoint_map['get_file_diff'].format(entity.org, entity.project, diff_parameters, repo_id)
            json_obj = get(endpoint, entity.pr_approver_key)
            blocks = json_obj['blocks']
            visited_lines = []
            for block in blocks:
                if block['changeType'] == 1 and block['mLine'] not in visited_lines:
                    self.changed_lines.append(block['mLines'])
                    visited_lines.append(block['mLine'])
        return self.changed_lines

    def changed_files_info(self):
        if not self.__changed_files_info:
            entity = self.entity
            endpoint = endpoint_map['pr_commits'].format(entity.org, entity.project, entity.repo(), entity.pr_num,
                                                         entity.ado_version)
            commits_obj = get(endpoint, entity.pat)
            commits = []
            visited_files = []
            for commit in commits_obj['value']:
                commits.append(commit['commitId'])
                changes_endpoint = endpoint_map['commit_changes'].format(entity.org, entity.project, entity.repo(),
                                                                         commit['commitId'], entity.ado_version)
                changes = get(changes_endpoint, entity.pat)
                for change in changes['changes']:
                    if change['item']['gitObjectType'] == 'blob' and change['item']['path'] not in visited_files:
                        self.__changed_files_info.append(change)
                        visited_files.append(change['item']['path'])
        return self.__changed_files_info

    def add_reviewer(self, reviewer, vote=0, is_required=True):
        response = None
        try:
            url = endpoint_map['approve_pr_by_id'].format(self.entity.org, self.entity.project, self.entity.repo(),
                                                          self.entity.pr_num, reviewer)
            querystring = {"api-version": self.entity.ado_version}
            body = {"vote": vote, "isRequired": is_required}

            response = put(url, self.entity.pat, querystring, payload=json.dumps(body))
            self.__logger.info(self.__name, "Added {}-reviewer {} successfully with vote {}!"
                               .format('required' if is_required else 'optional', reviewer, vote))
        except Exception:
            self.__logger.error(self.__name, 'Failed to add_reviewer({}) - API response: {}'.format(reviewer, response))
            raise FailedToAddReviewerError(reviewer)
