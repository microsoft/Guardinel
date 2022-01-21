# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from core.interfaces.notifier import Notifier


class CommandLineNotifier(Notifier):

    def notify(self, entity, result):
        print(result)

    def name(self):
        return 'cmdline_notifier'
