from src.data.seed_data import calls


def get_all_calls():
    return [call for call in calls if not call["is_archived"]]


def get_call_by_id(call_id):
    for call in calls:
        if call["id"] == call_id:
            return call
    return None
