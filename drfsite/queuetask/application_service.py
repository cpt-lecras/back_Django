from .models import QueueEntry, QueueEntryStatus, Human

queues: dict[int, QueueEntry] = {}

def create_queue(queue_id: int):
    if queue_id not in queues:
        que=QueueEntry(queue_id,[])
        queues[queue_id] = que
        return que
    return "Already exist"

def add_user_to_queue(queue_id: int, user_id: int) -> QueueEntry:

    if queue_id not in queues:
        create_queue(queue_id)
    que = queues[queue_id]
    if user_id not in queues[queue_id].user_ids:
        hum=Human(user_id)
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
    que=queues[queue_id]
    que.user_ids[user_id-1].status=QueueEntryStatus.NOTIFIED
    return que.user_ids[user_id-1]



def serve_user(queue_id: int, user_id: int):
    que = queues[queue_id]
    que.user_ids[user_id-1].status = QueueEntryStatus.SERVED
    return que.user_ids[user_id-1]