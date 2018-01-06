from _thread import RLock
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from queue import Queue
from sawtooth_signing import Signer
from sawtooth_validator.journal.block_cache import BlockCache
from sawtooth_validator.journal.block_wrapper import BlockWrapper
from sawtooth_validator.protobuf.batch_pb2 import Batch
from sawtooth_validator.protobuf.transaction_pb2 import (
    Transaction,
    TransactionHeader,
)
from test_journal.mock import (
    MockBlockSender,
    MockChainIdManager,
    MockPermissionVerifier,
    MockStateViewFactory,
    MockTransactionExecutor,
    SynchronousExecutor,
)
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)


def look_ahead(
    iterable: RepeatedCompositeFieldContainer
) -> Iterator[Tuple[Batch, bool]]: ...


class BlockValidator:
    def _compute_batch_change(
        self,
        new_chain: List[BlockWrapper],
        cur_chain: List[BlockWrapper]
    ) -> Union[Tuple[List[Batch], List[Batch]], Tuple[List[Batch], List[Any]]]: ...
    def _find_common_ancestor(
        self,
        new_blkw: BlockWrapper,
        cur_blkw: BlockWrapper,
        new_chain: List[BlockWrapper],
        cur_chain: List[BlockWrapper]
    ) -> None: ...
    def _find_common_height(
        self,
        new_chain: List[Any],
        cur_chain: List[Any]
    ) -> Tuple[BlockWrapper, BlockWrapper]: ...
    def _get_previous_block_root_state_hash(self, blkw: BlockWrapper) -> str: ...
    def _test_commit_new_chain(self) -> bool: ...
    def _txn_header(
        self,
        txn: Transaction
    ) -> TransactionHeader: ...
    def _validate_on_chain_rules(self, blkw: BlockWrapper) -> bool: ...
    def _validate_permissions(self, blkw: BlockWrapper) -> bool: ...
    def _verify_batch_transactions(self, batch: Batch) -> None: ...
    def _verify_block_batches(self, blkw: BlockWrapper) -> bool: ...
    def run(self) -> None: ...
    def validate_block(self, blkw: BlockWrapper) -> bool: ...


class ChainController:
    def __init__(
        self,
        block_cache: BlockCache,
        block_sender: MockBlockSender,
        state_view_factory: MockStateViewFactory,
        transaction_executor: MockTransactionExecutor,
        chain_head_lock: RLock,
        on_chain_updated: Callable,
        squash_handler: None,
        chain_id_manager: Optional[MockChainIdManager],
        identity_signer: Signer,
        data_dir: None,
        config_dir: None,
        permission_verifier: MockPermissionVerifier,
        chain_observers: List[Any],
        thread_pool: Optional[SynchronousExecutor] = None,
        metrics_registry: None = None
    ) -> None: ...
    def _make_receipts(self, results: List[Any]) -> List[Any]: ...
    def _set_chain_head_from_block_store(self) -> None: ...
    def _set_genesis(self, block: BlockWrapper) -> None: ...
    def _submit_blocks_for_verification(
        self,
        blocks: List[BlockWrapper]
    ) -> None: ...
    @property
    def chain_head(self) -> Optional[BlockWrapper]: ...
    def has_block(self, block_id: str): ...
    def on_block_received(self, block: BlockWrapper) -> None: ...
    def on_block_validated(
        self,
        commit_new_block: bool,
        result: Dict[str, Union[BlockWrapper, List[BlockWrapper], List[Batch], int]]
    ) -> None: ...
    def queue_block(self, block: BlockWrapper) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...


class _ChainThread:
    def __init__(
        self,
        chain_controller: ChainController,
        block_queue: Queue,
        block_cache: BlockCache
    ) -> None: ...
    def stop(self) -> None: ...
