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

from sawtooth_poet.poet_consensus.poet_block_publisher import PoetBlockPublisher
from sawtooth_poet.poet_consensus.poet_block_verifier import PoetBlockVerifier
from sawtooth_poet.poet_consensus.poet_fork_resolver import PoetForkResolver


LOGGER = logging.getLogger(__name__)


class PoetOracle:
    def __init__(self, service):
        block_cache = _BlockCacheProxy(service)
        state_view_factory = _StateViewFactoryProxy(service)

        # this needs a component endpoint (?)
        batch_publisher = _BatchPublisherProxy()

        # these should eventually be passed in
        data_dir = '/var/lib/sawtooth/'
        config_dir = '/etc/sawtooth/'
        validator_id = 'this-should-be-the-validator-public-key'

        self._publisher = PoetBlockPublisher(
            block_cache=block_cache,
            state_view_factory=state_view_factory,
            batch_publisher=batch_publisher,
            data_dir=data_dir,
            config_dir=config_dir,
            validator_id=validator_id)

        self._verifier = PoetBlockVerifier(
            block_cache=block_cache,
            state_view_factory=state_view_factory,
            data_dir=data_dir,
            config_dir=config_dir,
            validator_id=validator_id)

        self._fork_resolver = PoetForkResolver(
            block_cache=block_cache,
            state_view_factory=state_view_factory,
            data_dir=data_dir,
            config_dir=config_dir,
            validator_id=validator_id)

    def initialize_block(self, block):
        return self._publisher.initialize_block(block)

    def verify_block(self, block):
        return self._verifier.verify_block(block)

    def switch_forks(self, cur_fork_head, new_fork_head):
        '''"compare_forks" is not an intuitive name.'''
        return self._fork_resolver.compare_forks(cur_fork_head, new_fork_head)

class PoetBlock:
    def __init__(self, block):
        # fields that come with consensus blocks
        self.block_id = block.block_id
        self.previous_id = block.previous_id
        self.signer_id = block.signer_id
        self.block_num = block.block_num
        self.payload = block.payload
        self.summary = block.summary

        # fields that poet requires
        self.identifier = block.block_id
        self.previous_block_id = block.previous_id
        self.signer_public_key = block.signer_id.hex()

        # this is a trick
        self.state_root_hash = block.block_id


class _BlockCacheProxy:
    def __init__(self, service):
        self.block_store = _BlockStoreProxy(service)  # public
        self._service = service

    def __getitem__(self, block_id):
        return PoetBlock(self._service.get_blocks([block_id])[block_id])


class _BlockStoreProxy:
    def __init__(self, service):
        self._service = service

    @property
    def chain_head(self):
        return PoetBlock(self._service.get_chain_head())

    # this needs a component endpoint
    def get_block_by_transaction_id(self, transaction_id):
        pass

    def get_block_iter(self, reverse):
        # Ignore the reverse flag, since we can only get blocks
        # starting from the head.

        # where does the chain head come from?
        # block or block_id?
        chain_head = self.chain_head

        yield chain_head

        curr = chain_head

        # assume chain_head is a block (else get the block)
        while curr.previous_id:
            previous_block = PoetBlock(
                self._service.get_blocks([curr.previous_id]))

            yield previous_block

            curr = previous_block


class _StateViewFactoryProxy:
    def __init__(self, service):
        self._service = service

    def create_view(self, state_root_hash=None):
        '''The "state_root_hash" is really the block_id.'''

        block_id = state_root_hash

        return _StateViewProxy(self._service, block_id)


class _StateViewProxy:
    def __init__(self, service, block_id):
        self._service = service
        self._block_id = block_id

    def get(self, address):
        result = self._service.get_state(
            block_id=self._block_id,
            addresses=[address])

        LOGGER.error('StateViewProxy.get -- result: %s', result)

        return result[address]

    def leaves(self, prefix):
        return 'hello'


class _BatchPublisherProxy:
    def send(self, transactions):
        pass
