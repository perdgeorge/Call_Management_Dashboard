from src.core.schemas import CreateNoteSchema, GetCallSchema
from src.data.seed_data import calls
from src.models.call import Call
from src.core.exceptions import (
    CallInvalidDataError,
    CallNotFoundError,
    CallFilterNotFoundError,
)
from src.core.enums import CallType, CallDirection


def get_all_calls() -> list[GetCallSchema]:
    for call in calls:
        validate_call(call)
    return calls


def get_non_archived_calls() -> list[GetCallSchema]:
    calls_numbers = [call for call in calls if not call["is_archived"]]
    for number in calls_numbers:
        validate_call(number)
    return calls_numbers


def get_call_by_id(call_id: int) -> GetCallSchema:
    for call in calls:
        if call["id"] == call_id:
            return call
    raise CallNotFoundError(call_id)


def add_note_by_id(call_id: int, note: CreateNoteSchema) -> GetCallSchema:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if "notes" not in call:
                call.update({"notes": [note]})
                return call
            else:
                call["notes"].append(note)
                return call
    raise CallNotFoundError(call_id)


def archive_call_by_id(call_id: int) -> str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if call["is_archived"]:
                return f"Call with ID:{call_id} is already archived!"
            else:
                call["is_archived"] = True
                return f"Call with ID:{call_id} has been archived!"
    raise CallNotFoundError(call_id)


def unarchive_call_by_id(call_id: int) -> str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            if call["is_archived"] is True:
                call["is_archived"] = False
                return f"Call with ID:{call_id} has been unarchived!"
            else:
                return f"Call with ID:{call_id} is already unarchived!"
    raise CallNotFoundError(call_id)


def archive_all_calls() -> str:
    calls_numbers = [call for call in calls if not call["is_archived"]]
    for number in calls_numbers:
        number["is_archived"] = True
    return "All calls have been archived"


def filter_calls(call_filter: str) -> list[GetCallSchema]:
    Call_Directions = [direction.value for direction in CallDirection]
    Call_Types = [call_type.value for call_type in CallType]
    call_filter = call_filter.lower()
    all_calls = get_all_calls()
    if call_filter in Call_Types:
        return [call for call in all_calls if call["call_type"] == call_filter]
    elif call_filter in Call_Directions:
        return [call for call in all_calls if call["direction"] == call_filter]
    elif call_filter == "archived":
        return [call for call in all_calls if call["is_archived"] is True]
    elif call_filter == "not_archived":
        return [call for call in all_calls if call["is_archived"] is False]
    raise CallFilterNotFoundError(call_filter)


def delete_call_by_id(call_id: int) -> str:
    for call in calls:
        if call["id"] == call_id:
            validate_call(call)
            calls.remove(call)
            return f"Call with ID:{call_id} is deleted!"
    raise CallNotFoundError(call_id)


def validate_call(call: Call):
    Call_Directions = [direction.value for direction in CallDirection]
    Call_Types = [call_type.value for call_type in CallType]
    caller = call["from_number"].replace(" ", "")
    receiver = call["to_number"].replace(" ", "")
    if call["direction"] not in Call_Directions:
        raise CallInvalidDataError(
            call["direction"],
        )
    if call["call_type"] not in Call_Types:
        raise CallInvalidDataError(
            call["call_type"],
        )
    if type(call["duration"]) is not int:
        raise CallInvalidDataError("Error: A call's duration must be integer")
    if caller[0] != "+" or not caller[1:].isdigit():
        raise CallInvalidDataError(call["from_number"])
    if receiver[0] != "+" or not receiver[1:].isdigit():
        raise CallInvalidDataError(call["to_number"])
