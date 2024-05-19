import pytest
from queuetask.models import QueueEntry, QueueEntryStatus, Human
from queuetask.application_service import queues,create_queue,add_user_to_queue,get_queue_entries,notify_user,serve_user




def test_create_queue():
    queue_id = 1
    queue_entry = create_queue(queue_id)
    assert queue_entry.id == queue_id
    # Попытка создать очередь с существующим queue_id
    existing_queue = create_queue(queue_id)
    assert existing_queue == "Already exist"

def test_add_user_to_queue():
    queue_id = 2
    user_id = 1
    queue_entry = add_user_to_queue(queue_id, user_id)
    assert len(queue_entry.user_ids) == 1
    assert queue_entry.user_ids[0].id == user_id
    assert queue_entry.user_ids[0].status == QueueEntryStatus.WAITING

def test_get_queue_entries():
    ls=[Human(1),Human(2)]
    qu=QueueEntry(1,ls)
    queues[1]=qu
    res=get_queue_entries(1)
    assert len(res) == 2
    assert res[0].id == 1
    assert res[1].id == 2





