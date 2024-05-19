# operations_service.py
from uuid import uuid4
import uuid
from typing import Dict
from .models import Operation

operations: Dict[uuid.UUID, Operation] = {}


def create_operation() -> uuid.UUID:
    operation_id = uuid4()
    operations[operation_id] = Operation(operation_id)
    return operation_id


def finish_operation(operation_id: uuid.UUID, result: Dict):
    if operation_id not in operations:
        raise KeyError(f"Operation with id {operation_id} not found")

    operation = operations[operation_id]
    operation.done = True
    operation.result = result


def get_operation(operation_id: uuid.UUID) -> Operation:
    if operation_id not in operations:
        raise KeyError(f"Operation with id {operation_id} not found")

    return operations[operation_id]