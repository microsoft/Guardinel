# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json

from api_client.ado.constants import ADOConstants
from api_client.exceptions import FailedToAttachWorkItemError, FailedToUpdateFieldsError
from core.api.caller import get, patch, post
from api_client.ado.config import endpoint_map
from core.exceptions import APICallFailedError
from core.utils.map import resources


class FieldValueObject:
    """
    Object that will be used while making updates to a list of work items using patch calls
    """

    def __init__(self):
        self.payload = []

    def update_field(self, field_path, field_value):
        update_field = {
            "op": "add",
            "path": field_path,
            "value": field_value
        }
        self.payload.append(update_field)

    def remove_field(self, field_path):
        remove_field = {
            "op": "remove",
            "path": field_path,
        }
        self.payload.append(remove_field)

    def payload_str(self):
        return json.dumps(self.payload)


class WorkItemApiClient:
    __logger = resources.get('LOGGER')
    __name = 'WorkItemApiClient'

    def __init__(self, entity):
        self.entity = entity

    def get_work_items(self, items: list):
        items = []
        for wi in items:
            items.append(self.get_work_item_by_id(wi))
        return items

    def get_work_item_by_id(self, item_id):
        endpoint = endpoint_map['work_item_by_id'].format(self.entity.org, item_id)
        wi_data = get(endpoint, self.entity.pat)
        return wi_data

    def get_work_item_by_id_with_relations(self, work_item_id):
        endpoint = endpoint_map['work_item_by_id_with_relations'].format(self.entity.org, work_item_id)
        wi_data = get(endpoint, self.entity.pat)
        return wi_data

    def get_work_items_by_query_id(self, query_id):
        """
        retrieves query metadata from the query_id and returns the list of workitems
        """
        endpoint = endpoint_map['ado_query_by_id'] \
            .format(self.entity.org, self.entity.project, query_id, self.entity.ado_version)

        # retrieve query metadata
        query_md = get(endpoint, self.entity.pat)
        if query_md is None:
            raise ValueError("Couldn't retrieve query metadata for query_id : {}".format(query_id))

        # retrieve list of workitems which is the result of the query
        self.__logger.info(self.__name, "Query Filter Title: '{}'".format(query_md['name']))
        wi_results = get(query_md['_links']['wiql']['href'], self.entity.pat)

        if 'workItems' not in wi_results or wi_results['workItems'] is None or len(wi_results['workItems']) == 0:
            self.__logger.info(self.__name, 'no WorkItems found for query {}: {}'.format(query_id, query_md['name']))
            return []

        self.__logger.info(self.__name, 'Found {} WorkItem(s) for query filter "{}"...\n'
                           .format(len(wi_results['workItems']), query_md['name']))
        return wi_results['workItems']

    def attach_work_item(self, item_id, pr_entity, artifact_id):
        """
        Method to attach work item to PR, if work item is available in VSO URl, while PR doe not have link
        """
        url = endpoint_map['work_item_update_by_id'].format(pr_entity.org, "MSTeams", item_id)
        querystring = {"api-version": pr_entity.ado_version}
        payload = [{
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "ArtifactLink",
                "url": artifact_id,
                "attributes": {
                    "name": "Pull request"
                }
            }
        }]
        try:
            response = patch(url, pr_entity.pat, querystring, json.dumps(payload))
        except APICallFailedError as e:
            raise FailedToAttachWorkItemError(item_id)
        self.__logger.info(self.__name, "Attached work item successfully!" + response.text)

    def create(self, work_item_type, payload,
               query_string='{}',
               content_type='application/json-patch+json'):
        endpoint = endpoint_map['create_work_item'] \
            .format(self.entity.org, self.entity.project, work_item_type, self.entity.ado_version)

        resp = post(endpoint=endpoint,
                    pat=self.entity.pat,
                    query_str=query_string,
                    payload=payload,
                    content_type=content_type)

        return resp

    def linked_parent_work_items(self, work_item_id):
        json_response = self.get_work_item_by_id_with_relations(work_item_id)
        relations = json_response['relations']
        parent = []
        for relation in relations:
            self.__logger.debug(self.__name, 'Relation' + str(relation))
            if relation['rel'] == ADOConstants.work_item_relations['parent']:
                parent.append(relation['url'])
        return parent

    def update_fields(self, pr_entity, work_item_id, field_value_obj: FieldValueObject):
        payload = field_value_obj.payload_str()
        response = None
        querystring = {"api-version": pr_entity.ado_version}

        try:
            url = endpoint_map['work_item_by_id'].format(pr_entity.org, work_item_id)
            response = patch(url, pr_entity.pat, querystring, payload=payload)
            self.__logger.info(self.__name, "Successfully updated the fields {} for work item {}!"
                               .format(payload, work_item_id))
        except APICallFailedError:
            self.__logger.error(self.__name, "API response: {}".format(response.text if response else None))
            raise FailedToUpdateFieldsError(work_item_id, payload)
