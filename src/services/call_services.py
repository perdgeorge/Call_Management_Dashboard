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


def filter_calls(call_type):
    calls = get_all_calls()
    call_types = ["answered", "voicemail", "missed"]
    if call_type in call_types:
        return [call for call in calls if call["call_type"] == call_type]


def validate_call(call):
    if call["direction"] not in ("inbound", "outbound"):
        raise ValueError("Error: A call's direction must be Inbound or Outbound")
    if call["call_type"] not in ("answered", "voicemail", "missed"):
        raise ValueError(
            "Error: A call's call type must be either answered, voicemail or missed"
        )
    if type(call["duration"]) is not int:
        raise ValueError("Error: A call's duration must be integer")
    if call["from_number"][0] != "+" and call["from_number"][1:].isdigit() is False:
        raise ValueError(
            "Error: A call's from_number must have the format of +30 697 12 12 123"
        )
    if call["to_number"][0] != "+" and call["to_number"][1:].isdigit() is False:
        raise ValueError(
            "Error: A call's to_number must have the format of +30 697 12 12 123"
        )
