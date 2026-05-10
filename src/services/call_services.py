from src.data.seed_data import calls


def get_all_calls():
    for call in calls:
        validate_call(call)
    return calls


def get_non_archived_calls():
    calls_numbers = [call for call in calls if not call["is_archived"]]
    for number in calls_numbers:
        validate_call(number)
    return calls_numbers


def get_call_by_id(call_id):
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            return call
    return None


def archive_call(call_id):
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if call["is_archived"]:
                return f"Call with ID:{call_id} is already archived!"
            else:
                call["is_archived"] = True
                return f"Call with ID:{call_id} has been archived!"
    return f"Call with ID:{call_id} is not exist!"


def unarchive_call(call_id):
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if call["is_archived"] is True:
                call["is_archived"] = False
                return f"Call with ID:{call_id} has been unarchived!"
            else:
                return f"Call with ID:{call_id} is already unarchived!"
    return f"Call with ID:{call_id} is not exist!"


def delete_call(call_id):
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            calls.remove(call)
            return f"Call with ID:{call_id} is deleted!"
    return f"Call with ID:{call_id} is not exist!"


def filter_calls(filter):
    all_calls = get_all_calls()
    if filter in ("answered", "voicemail", "missed"):
        return [call for call in all_calls if call["call_type"] == filter]
    elif filter in ("outbound", "inbound"):
        return [call for call in all_calls if call["direction"] == filter]
    elif filter == "archived":
        return [call for call in all_calls if call["is_archived"] is True]
    elif filter == "not_archived":
        return [call for call in all_calls if call["is_archived"] is False]


def validate_call(call):
    if call["direction"] not in ("inbound", "outbound"):
        raise ValueError("Error: A call's direction must be Inbound or Outbound")
    if call["call_type"] not in ("answered", "voicemail", "missed"):
        raise ValueError(
            "Error: A call's call type must be either answered, voicemail or missed"
        )
    if type(call["duration"]) is not int:
        raise ValueError("Error: A call's duration must be integer")
    if call["from_number"][0] != "+" or call["from_number"][1:].isdigit() is False:
        raise ValueError(
            "Error: A call's from_number must have the format of +30 697 12 12 123"
        )
    if call["to_number"][0] != "+" or call["to_number"][1:].isdigit() is False:
        raise ValueError(
            "Error: A call's to_number must have the format of +30 697 12 12 123"
        )


def add_note(call_id, note: dict):
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if "notes" not in call:
                call.update({"notes": [note]})
                return call
            else:
                call["notes"].append(note)
                return call
