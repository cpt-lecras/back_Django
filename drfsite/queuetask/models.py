# models.py
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import List, Union


class QueueEntryStatus(Enum):
    WAITING = 'waiting'
    NOTIFIED = 'notified'
    SERVED = 'served'

class Human:
    id: int
    status: QueueEntryStatus
    def __init__(self, id: int):
        self.id = id
        self.status: QueueEntryStatus = QueueEntryStatus.WAITING
class QueueEntry:
    id: int
    user_ids: List[Human] = []
    created_at: datetime

    def __init__(self, id: int, user_ids: List[Human]):
        self.id = id
        self.user_ids = user_ids
        self.created_at = datetime.now()

class Operation:
    id: UUID
    done: bool
    result = None

    def __init__(self, id: UUID, done: bool = False, result = None):
        self.id = id
        self.done = done
        self.result = result