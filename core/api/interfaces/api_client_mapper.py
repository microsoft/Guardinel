# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod


class ClientMapper(ABC):
    """
    This mapper would provide a config dict that maps a key to relevant api_client
    """

    @abstractmethod
    def config(self):
        raise NotImplementedError('Please provide a mapping of api implementations!')
