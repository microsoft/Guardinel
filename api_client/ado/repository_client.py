# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.api.caller import get
from api_client.ado.endpoints import endpoint_map
from core.api.interfaces.repository_client import RepositoryApiClientInterface


class RepositoryClient(RepositoryApiClientInterface):

    def __init__(self):
        super().__init__()
        self.__name = 'RepositoryClient'

    def get_branches(self, entity, repo, contains=None):
        self.__logger.debug(self.__name, 'Retrieving branches for repo {}'.format(repo))
        endpoint = endpoint_map['repo_branches'].format(entity.org, entity.project, repo, entity.ado_version)
        if contains is not None:
            endpoint = '{}&filterContains={}'.format(endpoint, contains)

        data = get(endpoint, entity.pat)
        return data

    def get_file(self, entity, file_path, commit_id):
        """
        Returns the file version on the given commit id
        """
        self.__logger.debug(self.__name, 'Attempt to fetch {} of commit version: {}'.format(file_path, commit_id))
        endpoint = endpoint_map['file_from_commit'].format(
            entity.org, entity.project, entity.repo(), file_path, commit_id)
        resp = get(endpoint, entity.pat)
        return resp

    def get_commit_metadata(self, entity, commit_id):
        """
        Returns the metadata on the given commit id

        Commit metadata contains info on author, committer, pusher, commit description, parent commit id,
        links to changes introduced in the commit, etc
        """
        self.__logger.debug(self.__name, 'fetching metadata for commit id: {}'.format(commit_id))
        endpoint = endpoint_map['commit'].format(
            entity.org, entity.project, entity.repo(), commit_id, entity.ado_version)
        resp = get(endpoint, entity.pat)
        return resp
