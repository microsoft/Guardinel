# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from core.api.caller import get
from core.utils.map import resources


class RepositoryApiClientInterface(ABC):

    def __init__(self):
        self.__logger = resources.get('LOGGER')

    @abstractmethod
    def get_branches(self, entity, repo, contains=None):
        """
        Retrieves all the branch names of the repo that are matching the 'contains' string
        """
        raise NotImplementedError()

    @abstractmethod
    def get_file(self, entity, file_path, commit_id):
        """
        Returns the file on the given commit id
        """
        raise NotImplementedError()

    @abstractmethod
    def get_commit_metadata(self, entity, commit_id):
        """
        Returns the metadata on the given commit id

        Commit metadata contains info on author, committer, pusher, commit description, parent commit id,
        links to changes introduced in the commit, etc
        """
        raise NotImplementedError()
