from src.data.seed_data import calls
from src.models.call import Call, Note


def get_all_calls() -> list[Call]:
    for call in calls:
        validate_call(call)
    return calls


def get_non_archived_calls() -> list[Call]:
    calls_numbers = [call for call in calls if not call["is_archived"]]
    for number in calls_numbers:
        validate_call(number)
    return calls_numbers


def get_call_by_id(call_id: int) -> Call | str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            return call
    return f"Call with ID:{call_id} is not exist!"


def add_note(call_id: int, note: Note) -> Call | str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if "notes" not in call:
                call.update({"notes": [note]})
                return call
            else:
                call["notes"].append(note)
                return call
    return f"Call with ID:{call_id} is not exist!"


def archive_call(call_id: int) -> str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if call["is_archived"]:
                return f"Call with ID:{call_id} is already archived!"
            else:
                call["is_archived"] = True
                return f"Call with ID:{call_id} has been archived!"
    return f"Call with ID:{call_id} is not exist!"


def unarchive_call(call_id: int) -> str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if call["is_archived"] is True:
                call["is_archived"] = False
                return f"Call with ID:{call_id} has been unarchived!"
            else:
                return f"Call with ID:{call_id} is already unarchived!"
    return f"Call with ID:{call_id} is not exist!"


def filter_calls(call_filter: str) -> list[Call] | str:
    all_calls = get_all_calls()
    if call_filter in ("answered", "voicemail", "missed"):
        return [call for call in all_calls if call["call_type"] == call_filter]
    elif call_filter in ("outbound", "inbound"):
        return [call for call in all_calls if call["direction"] == call_filter]
    elif call_filter == "archived":
        return [call for call in all_calls if call["is_archived"] is True]
    elif call_filter == "not_archived":
        return [call for call in all_calls if call["is_archived"] is False]
    else:
        return "Error: Invalid filter! Filter must be either answered, voicemail, missed, outbound, inbound, archived or not_archived"


def delete_call(call_id: int) -> str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            calls.remove(call)
            return f"Call with ID:{call_id} is deleted!"
    return f"Call with ID:{call_id} is not exist!"


def validate_call(call: Call) -> str | None:
    caller = call["from_number"].replace(" ", "")
    receiver = call["to_number"].replace(" ", "")
    if call["direction"] not in ("inbound", "outbound"):
        raise ValueError("Error: A call's direction must be Inbound or Outbound")
    if call["call_type"] not in ("answered", "voicemail", "missed"):
        raise ValueError(
            "Error: A call's call type must be either answered, voicemail or missed"
        )
    if type(call["duration"]) is not int:
        raise ValueError("Error: A call's duration must be integer")
    if caller[0] != "+" or not caller[1:].isdigit():
        raise ValueError(
            "Error: A call's from_number must have the format of +30 697 1234567"
        )
    if receiver[0] != "+" or not receiver[1:].isdigit():
        raise ValueError(
            "Error: A call's to_number must have the format of +30 697 1234567"
        )
