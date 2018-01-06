from _thread import RLock
from queue import Queue
from sawtooth_signing import Signer
from sawtooth_validator.journal.batch_injector import DefaultBatchInjectorFactory
from sawtooth_validator.journal.block_builder import BlockBuilder
from sawtooth_validator.journal.block_cache import BlockCache
from sawtooth_validator.journal.block_store import BlockStore
from sawtooth_validator.journal.block_wrapper import BlockWrapper
from sawtooth_validator.journal.chain_commit_state import TransactionCommitCache
from sawtooth_validator.journal.consensus.dev_mode.dev_mode_consensus import BlockPublisher
from sawtooth_validator.protobuf.batch_pb2 import Batch
from sawtooth_validator.protobuf.block_pb2 import Block
from sawtooth_validator.protobuf.transaction_pb2 import Transaction
from test_journal.mock import (
    MockBatchInjector,
    MockBatchInjectorFactory,
    MockBatchSender,
    MockBlockSender,
    MockPermissionVerifier,
    MockScheduler,
    MockStateViewFactory,
    MockTransactionExecutor,
)
from test_journal.mock_consensus import BlockPublisher
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Union,
)


class BlockPublisher:
    def __init__(
        self,
        transaction_executor: MockTransactionExecutor,
        block_cache: BlockCache,
        state_view_factory: MockStateViewFactory,
        block_sender: MockBlockSender,
        batch_sender: Union[MockBlockSender, MockBatchSender],
        squash_handler: None,
        chain_head: Optional[BlockWrapper],
        identity_signer: Signer,
        data_dir: None,
        config_dir: None,
        permission_verifier: MockPermissionVerifier,
        check_publish_block_frequency: float,
        batch_observers: List[Any],
        batch_injector_factory: Optional[Union[DefaultBatchInjectorFactory, MockBatchInjectorFactory]] = None,
        metrics_registry: None = None
    ) -> None: ...
    def _build_candidate_block(self, chain_head: BlockWrapper) -> None: ...
    def _rebuild_pending_batches(
        self,
        committed_batches: Optional[List[Batch]],
        uncommitted_batches: Optional[List[Batch]]
    ) -> None: ...
    def _set_gauge(self, value: int) -> None: ...
    @property
    def chain_head_lock(self) -> RLock: ...
    def on_batch_received(self, batch: Batch) -> None: ...
    def on_chain_updated(
        self,
        chain_head: Optional[BlockWrapper],
        committed_batches: Optional[List[Batch]] = None,
        uncommitted_batches: Optional[List[Batch]] = None
    ) -> None: ...
    def on_check_publish_block(self, force: bool = False) -> None: ...
    def queue_batch(self, batch: Batch) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...


class _CandidateBlock:
    def __del__(self) -> None: ...
    def __init__(
        self,
        block_store: BlockStore,
        consensus: Union[BlockPublisher, BlockPublisher],
        scheduler: MockScheduler,
        committed_txn_cache: TransactionCommitCache,
        block_builder: BlockBuilder,
        max_batches: int,
        batch_injectors: List[MockBatchInjector]
    ) -> None: ...
    def _check_batch_dependencies(
        self,
        batch: Batch,
        committed_txn_cache: TransactionCommitCache
    ) -> bool: ...
    def _check_transaction_dependencies(
        self,
        txn: Transaction,
        committed_txn_cache: TransactionCommitCache
    ) -> bool: ...
    def _is_batch_already_committed(self, batch: Batch) -> bool: ...
    def _is_txn_already_committed(
        self,
        txn: Transaction,
        committed_txn_cache: TransactionCommitCache
    ) -> bool: ...
    def _poll_injectors(self, poller: Callable, batch_list: List[Any]) -> None: ...
    def _sign_block(
        self,
        block: BlockBuilder,
        identity_signer: Signer
    ) -> None: ...
    def add_batch(self, batch: Batch) -> None: ...
    @property
    def can_add_batch(self) -> bool: ...
    def check_publish_block(self) -> bool: ...
    def finalize_block(
        self,
        identity_signer: Signer,
        pending_batches: List[Any]
    ) -> Optional[Block]: ...
    def has_pending_batches(self) -> bool: ...
    @property
    def last_batch(self) -> Batch: ...


class _PublisherThread:
    def __init__(
        self,
        block_publisher: BlockPublisher,
        batch_queue: Queue,
        check_publish_block_frequency: float
    ) -> None: ...
    def stop(self) -> None: ...


class _RollingAverage:
    def __init__(self, sample_size: int, initial_value: int) -> None: ...
    @property
    def value(self) -> int: ...
