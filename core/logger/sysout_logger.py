# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.interfaces.logger import AbstractLogger


class SysoutLogger(AbstractLogger):
    """
    Concrete implementation of AbstractLogger
    TODO: Need to integrate with logging framework
    """
    def info(self, tag, message):
        print("[info] [{}] {}".format(tag, message))

    def error(self, tag, message):
        print("[error] [{}] {}".format(tag, message))

    def warn(self, tag, message):
        print("[warn] [{}] {}".format(tag, message))

    def debug(self, tag, message):
        if self.debug_enabled():
            print("[debug] [{}] {}".format(tag, message))
