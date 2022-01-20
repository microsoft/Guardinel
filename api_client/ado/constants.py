# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

class ADOConstants:
    """
    Constants specific to Azure Devops API clients and classes
    """

    work_item_relations = {
        'parent': 'System.LinkTypes.Hierarchy-Reverse',
        'child': 'System.LinkTypes.Hierarchy-Forward'
    }
