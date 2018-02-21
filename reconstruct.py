# Copyright 2018 Intel Corporation
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


import logging

import yappi

from sawtooth_validator.server import state_verifier
from sawtooth_validator.server.log import init_console_logging


LOGGER = logging.getLogger(__name__)


def main():
    init_console_logging()

    global_state_db, blockstore = state_verifier.get_databases(
        bind_network='tcp://eth08800',
        data_dir='/var/lib/sawtooth')

    yappi.set_clock_type('cpu')
    yappi.start()

    state_verifier.verify_state(
        global_state_db=global_state_db,
        blockstore=blockstore,
        bind_component='tcp://eth0:4004',
        scheduler_type='parallel',
    )

    stats = yappi.get_func_stats()
    stats.save(
        'reconstruct.callgrind',
        type='callgrind')


if __name__ == '__main__':
    main()
