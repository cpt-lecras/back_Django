import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../drfsite')))
import pytest
from queuetask.models import QueueEntry, QueueEntryStatus, Human
from queuetask.application_service import queues, create_queue, add_user_to_queue, get_queue_entries


@pytest.fixture
def test_appl():
    return 1
@pytest.fixture
def test_appluser():
    return [2,1]
def test_create_queue(test_appl):
    test_queue_entry = create_queue(test_appl)
    assert test_queue_entry.id == test_appl

def test_add_user_to_queue(test_appluser):
    test_queue_entry = add_user_to_queue(test_appluser[0], test_appluser[1])
    assert len(test_queue_entry.user_ids) == 1
    assert test_queue_entry.user_ids[0].status == QueueEntryStatus.WAITING
def test_get_queue_entries():
    queues[1] = QueueEntry(1, [Human(1), Human(2)])
    test_res=get_queue_entries(1)
    assert len(test_res) == 2
    assert test_res[0].id == 1
    assert test_res[1].id == 2





























class TestQueue:
    queues: dict[int, QueueEntry] = {}

    def create_queue(queue_id: int):
        if queue_id not in queues:
            que = QueueEntry(queue_id, [])
            queues[queue_id] = que
            return que
        return "Already exist"

    def add_user_to_queue(queue_id: int, user_id: int) -> QueueEntry:

        if queue_id not in queues:
            create_queue(queue_id)
        que = queues[queue_id]
        if user_id not in queues[queue_id].user_ids:
            hum = Human(user_id)
            que = queues[queue_id]
            que.user_ids.append(hum)
            return que
        return que

    def get_queue_entries(queue_id: int) -> []:

        if queue_id not in queues:
            return None
        else:
            que = queues[queue_id]
            return que.user_ids

    def notify_user(queue_id: int, user_id: int):
        que = queues[queue_id]
        que.user_ids[user_id - 1].status = QueueEntryStatus.NOTIFIED
        return que.user_ids[user_id - 1]

    def serve_user(queue_id: int, user_id: int):
        que = queues[queue_id]
        que.user_ids[user_id - 1].status = QueueEntryStatus.SERVED
        return que.user_ids[user_id - 1]

