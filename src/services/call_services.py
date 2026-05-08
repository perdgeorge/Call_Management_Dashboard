from src.data.seed_data import calls


def get_all_calls():
    return [call for call in calls if not call["is_archived"]]


def get_call_by_id(call_id):
    for call in calls:
        if call["id"] == call_id:
            return call
    return None


def archive_call(call_id):
    for call in calls:
        if call["id"] == call_id:
            if call["is_archived"]:
                return f"Call with ID:{call_id} is already archived!"
            else:
                call["is_archived"] = True
                return f"Call with ID:{call_id} has been archived!"
    return f"Call with ID:{call_id} is not exist!"


def unarchive_call(call_id):
    for call in calls:
        if call["id"] == call_id:
            if call["is_archived"] is True:
                call["is_archived"] = False
                return f"Call with ID:{call_id} has been unarchived!"
            else:
                return f"Call with ID:{call_id} is already unarchived!"
    return f"Call with ID:{call_id} is not exist!"


def delete_call(call_id):
    for call in calls:
        if call["id"] == call_id:
            calls.remove(call)
            return f"Call with ID:{call_id} is deleted!"
    return f"Call with ID:{call_id} is not exist!"
