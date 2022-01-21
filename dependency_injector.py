from api_client.ado.ado_client_mapper import ADOClientMapper
from core.exceptions import DependencyInjectionError


class DependencyInjector:
    """
    Provides the instances of the dependencies
    """

    class Constants:
        API_CLIENT_MAPPER = 'api_client_mapper'

    mapper = {
        Constants.API_CLIENT_MAPPER: ADOClientMapper(),
    }

    @staticmethod
    def get(key):
        instance = DependencyInjector.mapper.get(key)
        if instance is None:
            raise DependencyInjectionError(key)
        return instance
