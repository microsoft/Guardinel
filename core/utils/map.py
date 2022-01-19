# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from impl.sysout_logger import SysoutLogger

"""
defines the map of resources that will be used by various components of
the core and the wrapper
"""
resources = {
    "LOGGER": SysoutLogger(),
}
