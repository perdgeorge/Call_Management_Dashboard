from src.core.schemas import CallSchema, CreateNoteSchema, GetCallSchema
from src.data.seed_data import calls
from src.core.exceptions import (
    CallNotFoundError,
    CallFilterNotFoundError,
)
from src.core.enums import CallType, CallDirection
from src.models.call import Call

call_directions = [direction.value for direction in CallDirection]
call_types = [call_type.value for call_type in CallType]


def add_call(self, call: Call) -> GetCallSchema:
    self.db.add(call)
    self.db.commit()
    self.db.refresh(call)
    return GetCallSchema.model_validate(call)


def create_call(self, call_data: CallSchema) -> GetCallSchema:
    new_call = Call(
        direction=call_data.direction,
        from_number=call_data.from_number,
        to_number=call_data.to_number,
        call_type=call_data.call_type,
        duration=call_data.duration,
        created_at=call_data.created_at,
        is_archived=call_data.is_archived,
        notes=call_data.notes,
    )
    return self.add_call(new_call)


def get_all_calls() -> list[GetCallSchema]:
    return [GetCallSchema.model_validate(call) for call in calls]


def get_non_archived_calls() -> list[GetCallSchema]:
    calls_numbers = [GetCallSchema.model_validate(call) for call in calls]
    return [call for call in calls_numbers if not call.is_archived]


def get_call_by_id(call_id: int) -> GetCallSchema:
    for call in calls:
        if call["id"] == call_id:
            return GetCallSchema.model_validate(call)
    raise CallNotFoundError(call_id)


def add_note_by_id(call_id: int, note: CreateNoteSchema) -> GetCallSchema:
    for call in calls:
        GetCallSchema.model_validate(call)
        if call["id"] == call_id:
            if "notes" not in call:
                call.update({"notes": [note]})
                return call
            else:
                call["notes"].append(note)
                return call
    raise CallNotFoundError(call_id)


def archive_call_by_id(call_id: int) -> str:
    for call in calls:
        GetCallSchema.model_validate(call)
        if call["id"] == call_id:
            if call["is_archived"]:
                return f"Call with ID:{call_id} is already archived!"
            else:
                call["is_archived"] = True
                return f"Call with ID:{call_id} has been archived!"
    raise CallNotFoundError(call_id)


def unarchive_call_by_id(call_id: int) -> str:
    for call in calls:
        GetCallSchema.model_validate(call)
        if call["id"] == call_id:
            if call["is_archived"] is True:
                call["is_archived"] = False
                return f"Call with ID:{call_id} has been unarchived!"
            else:
                return f"Call with ID:{call_id} is already unarchived!"
    raise CallNotFoundError(call_id)


def archive_all_calls() -> str:
    [GetCallSchema.model_validate(call) for call in calls]
    calls_numbers = [call for call in calls if not call["is_archived"]]
    for number in calls_numbers:
        number["is_archived"] = True
    return "All calls have been archived"


def filter_calls(call_filter: str) -> list[GetCallSchema]:
    call_filter = call_filter.lower()
    all_calls = get_all_calls()
    if call_filter in call_types:
        return [call for call in all_calls if call.call_type == call_filter]
    elif call_filter in call_directions:
        return [call for call in all_calls if call.direction == call_filter]
    elif call_filter == "archived":
        return [call for call in all_calls if call.is_archived is True]
    elif call_filter == "not_archived":
        return [call for call in all_calls if call.is_archived is False]
    raise CallFilterNotFoundError(call_filter)


def delete_call_by_id(call_id: int) -> str:
    for call in calls:
        GetCallSchema.model_validate(call)
        if call["id"] == call_id:
            calls.remove(call)
            return f"Call with ID:{call_id} is deleted!"
    raise CallNotFoundError(call_id)
