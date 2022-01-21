# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import re

from components.constants import Constants
from core.api.api_config_constants import APIConfigConstants
from core.api.caller import get
from core.interfaces.input import InputEntity

from core.utils.helper import get_value, is_empty
from dependency_injector import DependencyInjector


class PullRequestEntity(InputEntity):
    """
    Concrete implementation of the InputEntity.
    Provides the pr_num which will be used to retrieve relevant PR data
    """
    __name = 'PullRequestEntity'

    def __init__(self, org, proj, version='6.0'):
        self.pr_num = None
        self.pat = None
        self.user_id = None
        self.pipeline_type = None
        self.org = org
        self.project = proj
        self.ado_version = version
        self.__metadata = None
        self.__work_items = None
        self.__work_items_md_map = None
        self.__area_paths = None
        self.__commits = None
        self.__commits_md_map = {}
        self.__changedFiles = None
        self.pr_approver_key = None
        self.pr_approver_user_id = None
        self.pr_diff = None
        self.api_client_mapper = DependencyInjector.get(DependencyInjector.Constants.API_CLIENT_MAPPER)

        self.__comment_threads = None
        self.__changed_files = []
        self.__changes = None
        self.__fileDiff = None
        self.__files_from_pr = {}

    def name(self):
        return self.__name

    def pr_link(self):
        _pr_link = 'https://{}.visualstudio.com/{}/_git/{}/pullrequest/{}' \
            .format(self.org, self.project, self.repo(), self.pr_num)
        return _pr_link

    def key(self):
        return self.pr_num

    def metadata(self):
        if self.__metadata is None:
            self.__metadata = self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT).data(self)

        return self.__metadata

    def title(self):
        return get_value(self.metadata(), ['title'])

    def author(self):
        return get_value(self.metadata(), ['createdBy', 'displayName'])

    def author_alias(self):
        return get_value(self.metadata(), ['createdBy', 'uniqueName'])

    def repo(self):
        return get_value(self.metadata(), ['repository', 'name'])

    def repo_id(self):
        return get_value(self.metadata(), ['repository', 'id'])

    def source_branch(self):
        return get_value(self.metadata(), ['sourceRefName'])

    def target_branch(self):
        return get_value(self.metadata(), ['targetRefName'])

    def linked_work_items(self):
        if self.__work_items is None:
            self.logger().info(self.__name, 'Fetching Work-Items tied to the PR {}...\n'.format(self.pr_num))
            additional_data = get(self.metadata()['url'], self.pat)
            self.__work_items = get(additional_data['_links']['workItems']['href'], self.pat)['value']
        return self.__work_items

    def linked_work_items_ids(self):
        """
        Returns list of ids of work items tied to the PR
        """
        work_items = []
        for work_item in self.linked_work_items():
            work_items.append(get_value(work_item, ['id']))

        return work_items

    def linked_work_items_metadata_map(self):
        if self.__work_items_md_map is None:
            wi_client = self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT)
            self.__work_items_md_map = dict()
            self.logger().info(self.__name, 'Fetching metadata of work-items linked to the PR {}...\n'
                               .format(self.pr_num))
            for wi in self.linked_work_items():
                self.__work_items_md_map[wi['id']] = wi_client.get_work_item_by_id(self, wi['id'])

        return self.__work_items_md_map

    def work_items_field_values(self, field_name):
        """
        This method returns field values of all the work items tied to the PR

        Ex: If PR is tied to 3 work items, calling this method with field_name 'System.WorkItemType' will return a
        map of work item type like below:
        {
            '1995246': "Bug", '2995231': "Feature", '1795245': "Task"
        }

        Note: If field doesn't exist in the work item, returns a map where work item is mapped to FIELD_NOT_FOUND
        """
        field_value_map = {}
        for key, metadata in self.linked_work_items_metadata_map().items():
            field_value_map[key] = get_value(metadata, ['fields', field_name], default=Constants.FIELD_NOT_FOUND)
        return field_value_map

    def linked_area_paths(self):
        if self.__area_paths is None:
            self.__area_paths = set()
            for wi in self.linked_work_items_metadata_map().values():
                self.__area_paths.add(wi['fields']['System.AreaPath'])
        return self.__area_paths

    def get_commits(self):
        if self.__commits is None:
            self.__commits = get_value(
                self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT).get_commits(self), ['value'])
        return self.__commits

    def get_commit_metadata(self, commit_id):
        if is_empty(self.__commits_md_map) or commit_id in self.__commits_md_map.keys():
            self.__commits_md_map[commit_id] = self.api_client_mapper.get(APIConfigConstants.REPO_API_CLIENT)\
                .get_commit_metadata(self, commit_id)
        return self.__commits_md_map.get(commit_id)

    def get_parent_commits(self):
        pr_oldest_commit = self.get_commits()[-1]
        commit_md = self.get_commit_metadata(get_value(pr_oldest_commit, ['commitId']))

        # returns list of parent commit-ids
        return get_value(commit_md, ['parents'])

    def get_latest_commit(self):
        return self.get_commits()[0]

    def is_cherry_pick(self):
        """ Returns True if the current PR is a cherry picked one """
        desc = get_value(self.metadata(), ['description'])
        pattern = re.compile('Cherry-picked from commit')
        if len(pattern.findall(desc)) > 0:
            return True

        return False

    def get_reviewers(self):
        return get_value(self.metadata(), ['reviewers'])

    def get_approvers(self):
        approvers = []
        for reviewer in self.get_reviewers():
            vote = get_value(reviewer, ['vote'])
            if vote == 10 or vote == 5:
                approvers.append(reviewer)
        return approvers

    def is_approved_by(self, reviewers: list):
        """ Returns True if any of the reviewers in the input list has approved the PR """
        if is_empty(reviewers):
            return True

        pr_approvers = json.dumps(self.get_approvers())
        for reviewer in reviewers:
            if reviewer in pr_approvers:
                self.logger().info(self.name(), '{} has approved the PR!'.format(reviewer))
                return True
        return False

    def add_reviewers(self, reviewers: list, vote=0, is_required=False):
        """
        Takes a list of email aliases as input and adds them as reviewer to the PR
        Note: You should make an entry in the ado_data for the new email aliases.
        """
        if reviewers is None or len(reviewers) == 0:
            return

        for reviewer in reviewers:
            reviewer_id = get_value(Constants.user_id_mapping, [reviewer, 'id'])
            if reviewer_id is None:
                self.logger().warn(self.name(), 'reviewer_id is not configured in ado_data for {}'.format(reviewer))
            else:
                self.__add_reviewer(reviewer_id, vote, is_required)

    def __add_reviewer(self, reviewer_id, vote, is_required):
        if reviewer_id not in json.dumps(self.get_reviewers()):
            self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT)\
                .add_reviewer(entity=self, reviewer=reviewer_id, vote=vote, is_required=is_required)

    def is_work_item_linked(self, work_item_id):
        """ Returns Ture if the given work item id is linked to the given PR """
        if self.linked_work_items() is not None:
            for work_item in self.linked_work_items():
                if work_item['id'] == work_item_id:
                    return True
        return False

    def get_comment_threads(self):
        if self.__comment_threads is None:
            self.__comment_threads = self.api_client_mapper.get(
                APIConfigConstants.PULL_REQUEST_API_CLIENT).get_comment_threads(self)
        return self.__comment_threads

    def changed_files(self):
        """
        Returns list of files changed in the PR
        """
        files = []
        for change in get_value(self.get_diff(), ['changes']):
            if get_value(change, ['item', 'gitObjectType']) == 'blob':
                files.append(get_value(change, ['item', 'path']))

        return files

    def get_diff(self):
        if self.pr_diff is None:
            self.pr_diff = self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT).get_diff(self)
        return self.pr_diff

    def changed_files_info(self):
        if not self.__changed_files:
            self.__changed_files = self.api_client_mapper.get(
                APIConfigConstants.PULL_REQUEST_API_CLIENT).changed_files_info(self)
        return self.__changed_files

    def changes(self, repo_id, commit_id):
        if self.__changes is None:
            self.__changes = self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT) \
                .changes(self, repo_id, commit_id)
        return self.__changes

    def get_file_add_diff(self, diff_parameters, repo_id):
        if self.__fileDiff is None:
            self.__fileDiff = self.api_client_mapper.get(APIConfigConstants.PULL_REQUEST_API_CLIENT)\
                .get_file_add_diff(self, diff_parameters, repo_id)
        return self.__fileDiff

    def fetch_file_from_pr(self, file_path):
        if get_value(self.__files_from_pr, [file_path]) is None:
            latest_commit = self.get_latest_commit()['commitId']
            file = self.api_client_mapper.get(APIConfigConstants.REPO_API_CLIENT)\
                .get_file(self, file_path, latest_commit)
            self.__files_from_pr[file_path] = file

        return get_value(self.__files_from_pr, [file_path])
