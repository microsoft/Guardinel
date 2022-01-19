# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Holds the util functions used by both core and policy_checker

def get_value(values, keys: list, default=None):
    """
    returns value from json based on given key hierarchy
    Ex:
        val_map = {'one' : {'two' : 123 }}
        get_value(val_map, ['one', 'two']) returns 123

    @param values: json object
    @param keys: list keys from the hierarchy tree
    @param default: default value to return if the key is not found
    @return: value if exists
            default otherwise
    """
    if values is None:
        return default

    for key in keys:
        if key in values:
            values = values[key]
        else:
            return default
    return values if keys else default


def put_value(root, keys: list, value):
    """
    Updates the given value into the root with the given key hierarchy
    Ex:
        my_dict = {}
        put_value(my_dict, ['aa', 'bb', 'cc'], 10)
        Result:
            my_dict = {
                "aa": {
                    "bb": {
                        "cc": 10
                    }
                }
            }

    @param root: dict object
    @param keys: list of keys in the hierarchical order
    @param value: value to add in the dict
    """
    for key in keys:
        if key is keys[-1]:
            root[key] = value
        else:
            if key not in root:
                root[key] = {}
            root = root[key]


def get_anchor(anchor_text, anchor_href):
    return '<a href="{}">{}</a>'.format(anchor_href, anchor_text)
