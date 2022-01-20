# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from api_client.ado.ado_client_mapper import ADOClientMapper


class APIClientConfig:
    api_client_mapper = ADOClientMapper()

    def mapper(self):
        return self.api_client_mapper

    def get_client(self, client_key):
        return self.mapper().config().get(client_key)
