from queuetask.application_service import create_queue,add_user_to_queue,get_queue_entries

queue_id = 2
create_queue(queue_id)
add_user_to_queue(queue_id,1)
add_user_to_queue(queue_id, 2)
res=get_queue_entries(queue_id)
print(res)
print(len(res))