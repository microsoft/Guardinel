# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import traceback
from json.decoder import JSONDecodeError

import requests
from requests.auth import HTTPBasicAuth
from requests.utils import requote_uri

from core.exceptions import APICallFailedError
from core.utils.map import resources

logger = resources.get('LOGGER')
tag = 'api_caller'


def validate_resp(endpoint, resp):
    if resp.status_code != 200:
        msg = 'API call to endpoint <b><u>{}</u></b> failed!<br><br>Code: {}<br>Reason: {}' \
            .format(truncate(endpoint), resp.status_code, resp.reason)
        logger.debug(tag, 'API call {} failed with error: {} - {}'.format(endpoint, msg, resp.content))
        logger.error(tag, traceback.format_exc())
        raise APICallFailedError(msg)


def truncate(endpoint):
    """
    Truncates endpoint to return only last three strings of endpoint
    Ex:
    For endpoint https://aaa.bb.com/dd/ee/ff/gg?input1=test, returns "/ee/ff/gg"
    """
    __endpoint_strs = endpoint.rsplit('?')[0].rsplit('/')
    __truncated_endpoint = '/{}/{}/{}'.format(__endpoint_strs[-3], __endpoint_strs[-2], __endpoint_strs[-1])
    return __truncated_endpoint


def get(endpoint, pat, params=None):
    """ Makes a get call to the given input """
    if params is None:
        params = {}

    try:
        endpoint = requote_uri(endpoint)  # Added encoding for network calls
        resp = requests.get(endpoint, auth=HTTPBasicAuth('', pat), params=params)
        logger.debug(tag, "GET request url: {}".format(resp.request.url))
        validate_resp(endpoint, resp)

        logger.debug(tag, resp.text)
        return resp.json()
    except JSONDecodeError as e:
        logger.debug(tag, 'Response retrieved from endpoint {} is not a json'.format(endpoint))
        raise
    except APICallFailedError as e:
        raise e
    except Exception as e:
        raise APICallFailedError('API call {} failed with error: \n"{}"'.format(truncate(endpoint), e))


def post(endpoint, pat, query_str, payload, content_type="application/json"):
    """ Makes a post call to the given input """
    resp = None
    headers = {
        'Content-Type': content_type,
    }

    try:
        endpoint = requote_uri(endpoint)  # Added encoding for network calls
        logger.debug(tag, "POST call to {}".format(endpoint))
        resp = requests.post(endpoint, auth=HTTPBasicAuth('', pat), headers=headers, data=payload, params=query_str)
        validate_resp(endpoint, resp)

        logger.debug(tag, resp.text)
        return resp
    except JSONDecodeError as e:
        logger.debug(tag, 'Response retrieved from endpoint {} is not a json'.format(endpoint))
        logger.error(tag, resp.text)
        raise
    except APICallFailedError as e:
        raise e
    except Exception as e:
        logger.error(tag, resp.text)
        raise


def patch(endpoint, pat, query_str, payload):
    """ Makes a put call to the given input """
    resp = None
    headers = {
        'Content-Type': "application/json-patch+json",
    }

    try:
        endpoint = requote_uri(endpoint)  # Added encoding for network calls
        logger.debug(tag, "PATCH call to {}".format(endpoint))
        resp = requests.patch(endpoint, auth=HTTPBasicAuth('', pat), headers=headers, data=payload, params=query_str)
        validate_resp(endpoint, resp)

        logger.debug(tag, resp.text)
        return resp
    except JSONDecodeError as e:
        logger.debug(tag, 'Response retrieved from endpoint {} is not a json'.format(endpoint))
        logger.error(tag, resp.text)
        raise
    except APICallFailedError as e:
        raise e
    except Exception as e:
        logger.error(tag, resp.text)
        raise APICallFailedError('API call {} failed with error: \n"{}"'.format(truncate(endpoint), e))


def put(endpoint, pat, query_str, payload):
    """ Makes a put call to the given input """
    resp = None
    headers = {
        'Content-Type': "application/json",
    }

    try:
        endpoint = requote_uri(endpoint)  # Added encoding for network calls
        logger.debug(tag, "PUT call to {}".format(endpoint))
        resp = requests.put(endpoint, auth=HTTPBasicAuth('', pat), headers=headers, data=payload, params=query_str)
        validate_resp(endpoint, resp)

        logger.debug(tag, resp.text)
        return resp
    except JSONDecodeError as e:
        logger.debug(tag, 'Response retrieved from endpoint {} is not a json'.format(endpoint))
        logger.error(tag, resp.text)
        raise
    except APICallFailedError as e:
        raise e
    except Exception as e:
        logger.error(tag, resp.text)
        raise APICallFailedError('API call {} failed with error: \n"{}"'.format(truncate(endpoint), e))
