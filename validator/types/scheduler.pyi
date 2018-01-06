from sawtooth_validator.execution.scheduler_parallel import ParallelScheduler
from sawtooth_validator.execution.scheduler_serial import SerialScheduler
from sawtooth_validator.protobuf.transaction_pb2 import Transaction
from threading import Condition
from typing import (
    List,
    Optional,
    Union,
)


class BatchExecutionResult:
    def __init__(self, is_valid: bool, state_hash: Optional[str]) -> None: ...


class SchedulerIterator:
    def __init__(
        self,
        scheduler: Union[ParallelScheduler, SerialScheduler],
        condition: Condition,
        start_index: int = 0
    ) -> None: ...
    def __next__(self): ...


class TxnExecutionResult:
    def __init__(
        self,
        signature: Union[str, bool],
        is_valid: Optional[bool],
        context_id: Optional[str] = None,
        state_hash: Optional[str] = None,
        state_changes: None = None,
        events: None = None,
        data: None = None,
        error_message: str = '',
        error_data: bytes = b''
    ) -> None: ...


class TxnInformation:
    def __init__(
        self,
        txn: Transaction,
        state_hash: str,
        base_context_ids: List[str]
    ) -> None: ...
