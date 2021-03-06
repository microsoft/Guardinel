# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

class GuardinelError(Exception):
    """
    Parent error class for all the exceptions thrown by the system
    """
    def __init__(self, title=None, message=None, suggestion=None):
        if title is None:
            title = self.__class__.__name__
        self.title = title
        self.message = message
        self.suggestion = suggestion


class APICallFailedError(GuardinelError):
    """
    Exception thrown when call to an API endpoint fails
    """
    def __init__(self, message='Call to API endpoint failed!'):
        super().__init__()
        self.message = message
        self.suggestion = 'Could be an intermittent issue. Please re-queue the gate again after an hour.'


class MetricsError(GuardinelError):
    """ Parent class for all metrics error """
    pass


class UnknownMetricTypeError(MetricsError):
    def __init__(self, value):
        super().__init__()
        self.message = 'Unknown value type {} encountered while adding metrics!'.format(type(value))
        self.suggestion = 'Please reach out to Guardinel team to add an implementation for the type {}'\
            .format(type(value))


class DependencyInjectionError(GuardinelError):
    """
    Error that is thrown when dependency injection for a key is not found
    """
    def __init__(self, key):
        super().__init__()
        self.message = 'No dependency is injected for the key : {}'.format(key)
        self.suggestion = 'Please update the dependency mapping for {} in DependencyInjector'.format(key)
