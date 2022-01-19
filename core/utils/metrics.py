# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.exceptions import UnknownMetricTypeError
from core.interfaces.metrics import Metrics


class StringMetrics(Metrics):
    """ Represents the string values """

    def __init__(self, name, data):
        super().__init__(name, data)

    def append(self, value):
        if isinstance(value, int):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError('Expecting string/integer to concatenate but got {}'.format(value))

        self.data = self.data + value


class IntegerMetrics(Metrics):
    """ Represents the metrics that are of number type and can be modified """

    def __init__(self, name, data):
        super().__init__(name, data)

    def append(self, value):
        if not isinstance(value, int):
            raise TypeError('Expecting integer but got {} ({})'.format(value, type(value)))
        self.data += value


class ListMetrics(Metrics):

    def __init__(self, name, data=None):
        if data is None:
            data = []
        super().__init__(name, list(data))

    def append(self, append_value):
        if not isinstance(append_value, list):
            raise TypeError('Expecting list in append operation but got {}'.format(append_value))

        self.data.append(append_value)


class DictMetrics(Metrics):

    def __init__(self, name, data=None):
        if data is None:
            data = {}
        super().__init__(name, data.copy())

    def append(self, append_value):
        if not isinstance(append_value, dict):
            raise TypeError('Expecting dict in append operation but got {}'.format(append_value))

        self.data.update(append_value)


class MetricsData(Metrics):
    """
    Metrics Data Object that helps manage all the MetricsData of a Task
    """
    sub_metrics_delimiter = '.'

    def __init__(self, name, data=None):
        if data is None:
            data = {}
        super().__init__(name, data)

    def append(self, kwargs):
        """
        Adds the given key value pairs to the metrics data. Based on the type of the value, an appropriate metrics
        object will be created and inserted into the value
        """
        if not isinstance(kwargs, dict):
            raise TypeError('Expecting dict in append operation but got {}'.format(kwargs))
        if len(kwargs) == 0:
            return

        for name, value in kwargs.items():
            self.add(name, value)

    def add(self, key, value):
        if value is None:
            value = ''
        if isinstance(value, int):
            self.data[key] = IntegerMetrics(key, value)
        elif isinstance(value, str):
            self.data[key] = StringMetrics(key, value)
        elif isinstance(value, dict):
            self.data[key] = DictMetrics(key, value)
        elif isinstance(value, list) or isinstance(value, set):
            self.data[key] = ListMetrics(key, value)
        else:
            raise UnknownMetricTypeError(value)

    def add_metrics(self, metrics):
        if not isinstance(metrics, Metrics):
            raise TypeError('Only a Metrics object should be added to the MetricsData! Received {}'
                            .format(type(metrics)))
        self.data[metrics.name] = metrics

    def update(self, metrics_name, append_value):
        if self.data.get(metrics_name):
            self.data.get(metrics_name).append(append_value)
        else:
            self.append({metrics_name: append_value})

    def get(self, key):
        return self.data.get(key)

    def sub_metrics(self, name):
        md = MetricsData(self.name + self.sub_metrics_delimiter + name)
        md.__copy_basic_fields(self)
        self.add_metrics(md)
        return md

    def remove(self, key):
        return self.data.pop(key)

    def value(self):
        return self.data

    def update_basic_fields(self, entity):
        basic_fields = {'org': entity.org, 'project': entity.project, 'repository': entity.repo(),
                        'pull_request_id': entity.pr_num, 'pr_title': entity.title(), 'committer_name': entity.author(),
                        'committer_alias': entity.author_alias(), 'source_branch': entity.source_branch(),
                        'target_branch': entity.target_branch(), 'work_items': entity.linked_work_items(),
                        'area_paths': entity.linked_area_paths()}
        self.append(basic_fields)

    def __copy_basic_fields(self, copy_from):
        basic_fields = ['org', 'project', 'repository', 'pull_request_id', 'pr_title', 'committer_name',
                        'committer_alias', 'source_branch', 'target_branch', 'work_items', 'area_paths']
        for field in basic_fields:
            self.add_metrics(copy_from.get(field))
