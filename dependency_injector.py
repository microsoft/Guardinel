# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from api_client.ado.ado_client_mapper import ADOClientMapper
from components.config_builder import PoliciesConfigBuilder
from core.exceptions import DependencyInjectionError


class DependencyInjector:
    """
    Provides the instances of the dependencies
    """

    class Constants:
        API_CLIENT_MAPPER = 'api_client_mapper'
        CONFIG_BUILDER = 'config_builder'

    mapper = {
        Constants.API_CLIENT_MAPPER: ADOClientMapper(),
        Constants.CONFIG_BUILDER: PoliciesConfigBuilder()
    }

    @staticmethod
    def get(key):
        instance = DependencyInjector.mapper.get(key)
        if instance is None:
            raise DependencyInjectionError(key)
        return instance
