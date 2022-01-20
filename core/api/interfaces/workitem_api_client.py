# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
from abc import ABC, abstractmethod

from core.api.caller import get, patch, post
from api_client.ado.endpoints import endpoint_map
from core.utils.map import resources


class FieldValueObject(ABC):
    """
    Object that will be used while making updates to a list of work items using patch calls
    """

    @abstractmethod
    def update_field(self, field_path, field_value):
        raise NotImplementedError()

    @abstractmethod
    def remove_field(self, field_path):
        raise NotImplementedError()

    @abstractmethod
    def payload_str(self):
        raise NotImplementedError()


class WorkItemApiClient(ABC):

    def __init__(self):
        self.__logger = resources.get('LOGGER')

    @abstractmethod
    def get_work_items(self, entity, items: list):
        """
        Retrieves the work item metadata for all the work-items ids provided in the param
        """
        raise NotImplementedError()

    @abstractmethod
    def get_work_item_by_id(self, entity, item_id):
        """
        Retrieves the work item metadata for the given work-item id provided in the param
        """
        raise NotImplementedError()

    @abstractmethod
    def get_work_item_by_id_with_relations(self, entity, work_item_id):
        """
        Retrieves the work item metadata alone with the relations like PRs, links, wikis, etc
        """
        raise NotImplementedError()

    @abstractmethod
    def get_work_items_by_query_id(self, entity, query_id):
        """
        retrieves query metadata from the query_id and returns the list of workitems
        """
        raise NotImplementedError()

    @abstractmethod
    def attach_work_item(self, item_id, pr_entity, artifact_id):
        """
        Method to attach work item to PR, if work item is available in VSO URl, while PR doe not have link
        """
        raise NotImplementedError()

    @abstractmethod
    def create(self, entity, work_item_type, payload,
               query_string='{}',
               content_type='application/json-patch+json'):
        """
        Creates a new work item using the given payload
        """
        raise NotImplementedError()

    @abstractmethod
    def linked_parent_work_items(self, entity, work_item_id):
        """
        Returns the parent work items of the given work item id
        """
        raise NotImplementedError()

    @abstractmethod
    def update_fields(self, pr_entity, work_item_id, field_value_obj: FieldValueObject):
        """
        Updates the key-values of the FieldValueObject in the given work item
        """
        raise NotImplementedError()
