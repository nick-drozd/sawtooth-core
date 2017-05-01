# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import json

from sawtooth_lisp.lisp import LISP_NAMESPACE
from lisp_test.lisp_message_factory import LispMessageFactory
from sawtooth_integration.tests.integration_tools import RestClient


class LispClient(RestClient):
    def __init__(self, url):
        super().__init__(url, LISP_NAMESPACE)
        self.factory = LispMessageFactory()

    def define(self, name, expr):
        return self._send_lisp_txn(
            'define', name, expr)

    def step(self, name):
        return self._send_lisp_txn(
            'step', name, '')

    def show(self, name):
        return self.get_leaf(self.make_address(name)).decode()

    def list(self):
        pass

    def get_register(self, name, register):
        return json.loads(
            self.show(name))[register]

    def check_result(self, name):
        return self.get_register(name, 'val')

    def is_done(self, name):
        return self.get_register(name, 'instr') == 'DONE'

    def _send_lisp_txn(self, cmd, name, expr=''):
        return self.send_batches(
            self.factory.create_batch(
                cmd, name, expr))

    def make_address(self, name):
        return self.factory.name_to_address(name)
