from sawtooth_validator.journal.block_wrapper import BlockWrapper
from sawtooth_validator.networking.dispatch import HandlerResult
from sawtooth_validator.protobuf.batch_pb2 import Batch
from test_responder.mock import (
    MockCompleter,
    MockGossip,
)
from typing import Optional


class BatchByBatchIdResponderHandler:
    def __init__(
        self,
        responder: Responder,
        gossip: MockGossip
    ) -> None: ...
    def handle(self, connection_id: str, message_content: bytes) -> HandlerResult: ...


class BatchByTransactionIdResponderHandler:
    def __init__(
        self,
        responder: Responder,
        gossip: MockGossip
    ) -> None: ...
    def handle(self, connection_id: str, message_content: bytes) -> HandlerResult: ...


class BlockResponderHandler:
    def __init__(
        self,
        responder: Responder,
        gossip: MockGossip
    ) -> None: ...
    def handle(self, connection_id: str, message_content: bytes) -> HandlerResult: ...


class Responder:
    def __init__(
        self,
        completer: MockCompleter,
        cache_keep_time: int = 300,
        cache_purge_frequency: int = 30
    ) -> None: ...
    def add_request(self, requested_id: str, connection_id: str) -> None: ...
    def already_requested(self, requested_id: str): ...
    def check_for_batch(self, batch_id: str) -> Optional[Batch]: ...
    def check_for_batch_by_transaction(
        self,
        transaction_id: str
    ) -> Optional[Batch]: ...
    def check_for_block(self, block_id: str) -> Optional[BlockWrapper]: ...
    def get_request(self, requested_id: str): ...
    def remove_request(self, requested_id: str) -> None: ...


class ResponderBatchResponseHandler:
    def __init__(
        self,
        responder: Responder,
        gossip: MockGossip
    ) -> None: ...
    def handle(self, connection_id: str, message_content: bytes) -> HandlerResult: ...


class ResponderBlockResponseHandler:
    def __init__(
        self,
        responder: Responder,
        gossip: MockGossip
    ) -> None: ...
    def handle(self, connection_id: str, message_content: bytes) -> HandlerResult: ...
