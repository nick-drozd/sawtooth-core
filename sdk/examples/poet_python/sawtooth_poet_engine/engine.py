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
# -----------------------------------------------------------------------------

import logging
import queue
import time

from sawtooth_sdk.consensus.engine import Engine
from sawtooth_sdk.consensus import exceptions
from sawtooth_sdk.protobuf.validator_pb2 import Message

from sawtooth_poet_engine.oracle import PoetOracle, PoetBlock


LOGGER = logging.getLogger(__name__)

POET_INITIALIZE = 1
POET_PUBLISH = 1
POET_FINALIZE = 0
POET_VERIFY = 1
POET_FORK = 0


class PoetEngine(Engine):
    def __init__(self):
        # components
        self._service = None
        self._oracle = None

        # state variables
        self._exit = False
        self._published = False
        self._building = False

        time.sleep(10)

    def name(self):
        return 'PoET'

    def version(self):
        return '0.1'

    def stop(self):
        self._exit = True

    def _initialize_block(self):
        chain_head = self._get_chain_head()

        if not POET_INITIALIZE:
            self._service.initialize_block(chain_head.block_id)
            return True

        try:
            initialize = self._oracle.initialize_block(chain_head)
        except exceptions.InvalidState as err:
            LOGGER.warning(err)
            return False
        except Exception as err:
            LOGGER.exception('_initialize_block')
            return False

        if initialize:
            LOGGER.warning('initialize succeeded')
            self._service.initialize_block(chain_head.block_id)
        else:
            LOGGER.warning('initialization failed')

        return initialize

        # self._service.initialize_block(chain_head.block_id)

    def _check_consensus(self, block):
        if not POET_VERIFY:
            return True

        verify = self._oracle.verify_block(block)

        LOGGER.info('PoET verification: %s', verify)

        # TODO: this should return the verifier's result
        return True

    def _switch_forks(self, current_head, new_head):
        if not POET_FORK:
            return True

        try:
            return self._oracle.switch_forks(current_head, new_head)
        except TypeError as err:
            LOGGER.error('PoET fork error: %s', err)
        except:
            LOGGER.exception('switch_forks')

        return True

    def _check_block(self, block_id):
        self._service.check_blocks([block_id])

    def _fail_block(self, block_id):
        self._service.fail_block(block_id)

    def _get_chain_head(self):
        return PoetBlock(self._service.get_chain_head())

    def _get_block(self, block_id):
        return PoetBlock(self._service.get_blocks([block_id])[block_id])

    def _commit_block(self, block_id):
        self._service.commit_block(block_id)

    def _ignore_block(self, block_id):
        self._service.ignore_block(block_id)

    def _cancel_block(self):
        try:
            self._service.cancel_block()
        except exceptions.InvalidState:
            pass

    def _summarize_block(self):
        try:
            return self._service.summarize_block()
        except (exceptions.InvalidState, exceptions.BlockNotReady) as err:
            LOGGER.warning(err)
            return None

    def _finalize_block(self):
        time.sleep(1)

        summary = self._summarize_block()

        if summary is None:
            LOGGER.warning('No summary available')
            return None
        else:
            LOGGER.warning('summary: %s', summary)

        if POET_FINALIZE:
            try:
                consensus = self._oracle.finalize_block(summary)
            except ValueError as err:
                LOGGER.warning(err)
                consensus = None
            except:
                LOGGER.exception('finalize')

            if not consensus:
                return None
        else:
            consensus = summary

        while True:
            try:
                block_id = self._service.finalize_block(consensus)
                LOGGER.info('finalized %s with %s', block_id, consensus)
                return block_id
            except exceptions.BlockNotReady:
                time.sleep(1)
                continue
            except exceptions.InvalidState:
                return None

    def _check_publish_block(self):
        if not POET_PUBLISH:
            return True

        # Publishing is based solely on wait time, so just give it None.
        publish = self._oracle.check_publish_block(None)

        LOGGER.info('PoET publishing: %s', publish)

        return publish

    def start(self, updates, service, chain_head, peers):
        self._service = service
        self._oracle = PoetOracle(service)

        # 1. Wait for an incoming message.
        # 2. Cnheck for exit.
        # 3. Handle the message.
        # 4. Check for publishing.

        handlers = {
            Message.CONSENSUS_NOTIFY_BLOCK_NEW: self._handle_new_block,
            Message.CONSENSUS_NOTIFY_BLOCK_VALID: self._handle_valid_block,
            Message.CONSENSUS_NOTIFY_BLOCK_COMMIT:
                self._handle_committed_block,
        }

        while True:
            try:
                type_tag, data = updates.get(timeout=1)

                try:
                    handle_message = handlers[type_tag]
                except KeyError:
                    pass
                else:
                    handle_message(data)

            except queue.Empty:
                pass
                LOGGER.debug('empty queue')

            if self._exit:
                break

            ##########

            # publisher activity #

            if self._published:
                LOGGER.warning('already published at this height')
                continue

            if not self._building:
                LOGGER.warning('not building: attempting to initialize')
                if self._initialize_block():
                    self._building = True

            if self._building:
                LOGGER.warning('building: attempting to publish')
                if self._check_publish_block():
                    LOGGER.warning('finalizing block')
                    self._finalize_block()
                    self._published = True
                    self._building = False

    def _handle_new_block(self, block):
        block = PoetBlock(block)

        LOGGER.info('Checking consensus data: %s', block)

        if self._check_consensus(block):
            LOGGER.info('Passed consensus check: %s', block)
            self._check_block(block.block_id)
        else:
            LOGGER.info('Failed consensus check: %s', block)
            self._fail_block(block.block_id)

    def _handle_valid_block(self, block_id):
        block = self._get_block(block_id)

        chain_head = self._get_chain_head()

        LOGGER.info(
            'Choosing between chain heads -- current: %s -- new: %s',
            chain_head.block_id,
            block_id)

        if self._switch_forks(chain_head, block):
            LOGGER.info('Committing %s', block_id)
            self._commit_block(block_id)
        else:
            LOGGER.info('Ignoring %s', block_id)
            self._ignore_block(block_id)

    def _handle_committed_block(self, _block_id):
        chain_head = self._get_chain_head()

        LOGGER.info(
            'Chain head updated to %s, abandoning block in progress',
            chain_head.block_id)

        self._cancel_block()

        self._building = False
        self._published = False
