from sqlalchemy.orm import Session
from src.core.schemas import CallSchema, GetNoteSchema, GetCallSchema
from src.core.exceptions import (
    CallNotFoundError,
    CallFilterNotFoundError,
)
from src.core.enums import CallType, CallDirection
from src.models.call import Call
from src.models.note import Note

call_directions = [direction.value for direction in CallDirection]
call_types = [call_type.value for call_type in CallType]


def add_call(db: Session, call: Call) -> GetCallSchema:
    db.add(call)
    db.commit()
    db.refresh(call)
    return GetCallSchema.model_validate(call)


def create_call(db: Session, call_data: CallSchema) -> GetCallSchema:
    new_call = Call(
        direction=call_data.direction,
        from_number=call_data.from_number,
        to_number=call_data.to_number,
        call_type=call_data.call_type,
        duration=call_data.duration,
        is_archived=call_data.is_archived,
        notes=[Note(content=notes.content) for notes in call_data.notes]
        if call_data.notes
        else [],
    )
    return add_call(db, new_call)


def get_all_calls(db: Session) -> list[GetCallSchema]:
    calls = db.query(Call).order_by(Call.id.asc()).all()
    return [GetCallSchema.model_validate(call) for call in calls]


def get_non_archived_calls(db: Session) -> list[GetCallSchema]:
    calls = (
        db.query(Call).filter(Call.is_archived.is_(False)).order_by(Call.id.asc()).all()
    )
    return [GetCallSchema.model_validate(call) for call in calls]


def get_call_by_id(db: Session, call_id: int) -> GetCallSchema:
    call = db.query(Call).filter(Call.id == call_id).first()
    if call:
        return GetCallSchema.model_validate(call)
    raise CallNotFoundError(call_id)


def create_note(db: Session, note: Note) -> GetNoteSchema:
    new_note = Note(content=note.content, call_id=note.call_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return GetNoteSchema.model_validate(new_note)


def add_note_by_id(db: Session, call_id: int, new_note: GetNoteSchema) -> GetCallSchema:
    call = db.query(Call).filter(Call.id == call_id).first()
    if call:
        call.notes.append(Note(content=new_note.content, call_id=call_id))
        db.commit()
        db.refresh(call)
        return GetCallSchema.model_validate(call)
    raise CallNotFoundError(call_id)


def archive_call_by_id(db: Session, call_id: int) -> str:
    call = db.query(Call).filter(Call.id == call_id).first()
    if call:
        if call.is_archived:
            return f"Call with ID:{call_id} is already archived!"
        call.is_archived = True
        db.commit()
        return f"Call with ID:{call_id} has been archived!"
    raise CallNotFoundError(call_id)


def unarchive_call_by_id(db: Session, call_id: int) -> str:
    call = db.query(Call).filter(Call.id == call_id).first()
    if call:
        if call.is_archived is True:
            call.is_archived = False
            db.commit()
            return f"Call with ID:{call_id} has been unarchived!"
        return f"Call with ID:{call_id} is already unarchived!"
    raise CallNotFoundError(call_id)


def archive_all_calls(db: Session) -> str:
    calls = db.query(Call).all()
    for call in calls:
        call.is_archived = True
    db.commit()
    return "All calls have been archived"


def filter_calls(db: Session, call_filter: str) -> list[GetCallSchema]:
    call_filter = call_filter.lower()
    if call_filter in call_types:
        return (
            db.query(Call)
            .filter(Call.call_type == call_filter)
            .order_by(Call.id.asc())
            .all()
        )
    elif call_filter in call_directions:
        return (
            db.query(Call)
            .filter(Call.call_direction == call_filter)
            .order_by(Call.id.asc())
            .all()
        )
    elif call_filter == "archived":
        return (
            db.query(Call)
            .filter(Call.is_archived.is_(True))
            .order_by(Call.id.asc())
            .all()
        )
    elif call_filter == "not_archived":
        return (
            db.query(Call)
            .filter(Call.is_archived.is_(False))
            .order_by(Call.id.asc())
            .all()
        )
    raise CallFilterNotFoundError(call_filter)


def delete_call_by_id(db: Session, call_id: int) -> str:
    call = db.query(Call).filter(Call.id == call_id).first()
    if call:
        db.delete(call)
        db.commit()
        return f"Call with ID:{call_id} is deleted!"
    raise CallNotFoundError(call_id)
