# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
from abc import ABC, abstractmethod

from core.utils.map import resources


class PullRequestApiClientInterface(ABC):

    def __init__(self):
        self.__logger = resources.get('LOGGER')

    @abstractmethod
    def data(self):
        """
        Should return json metadata retrieved from the PR api call
        """
        raise NotImplementedError()

    @abstractmethod
    def get_creator(self):
        """
        Returns the creator of the PR. If necessary, we can reuse the data() function
        """
        raise NotImplementedError()

    @abstractmethod
    def get_creator_alias(self):
        """
        Returns the creator alias. This is an extension of the function get_creator()
        """
        raise NotImplementedError()

    @abstractmethod
    def get_work_items(self):
        """
        Retrieves the work-items tied to the pull request
        """
        raise NotImplementedError()

    @abstractmethod
    def get_comment_threads(self):
        """
        Returns the json which holds the comments threads
        """
        raise NotImplementedError()

    @abstractmethod
    def get_commits(self):
        """
        Returns the list of commits in the current PR
        """
        raise NotImplementedError()

    @staticmethod
    def get_diff(_entity):
        """
        Returns the files modified in the given entity
        """
        raise NotImplementedError()

    @abstractmethod
    def changes(self, repo_id, commit_id):
        """
        Returns list of files changes in the given commit-id
        """
        raise NotImplementedError()

    @abstractmethod
    def get_file_add_diff(self, diff_parameters, repo_id):
        """
        Returns list diff of a file
        """
        raise NotImplementedError()

    @abstractmethod
    def changed_files_info(self):
        """
        Returns list of changes files with their metadata
        """
        raise NotImplementedError()

    @abstractmethod
    def add_reviewer(self, reviewer, vote=0, is_required=True):
        """
        Adds the given reviewer to the PR. It will be made optional/required based on the is_required flag
        """
        raise NotImplementedError()
