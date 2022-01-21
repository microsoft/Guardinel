# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from api_client.ado.ado_pr_api_client import AdoPullRequestClient
from api_client.ado.ado_repository_api_client import AdoRepositoryClient
from api_client.ado.ado_work_item_api_client import AdoWorkItemClient
from core.api.api_config_constants import APIConfigConstants
from core.api.interfaces.api_client_mapper import ClientMapper


class ADOClientMapper(ClientMapper):

    client_mapper = {
        APIConfigConstants.REPO_API_CLIENT: AdoRepositoryClient(),
        APIConfigConstants.WORK_ITEM_API_CLIENT: AdoWorkItemClient(),
        APIConfigConstants.PULL_REQUEST_API_CLIENT: AdoPullRequestClient()
    }

    def config(self):
        return ADOClientMapper.client_mapper

    def get(self, key):
        return self.config().get(key)
