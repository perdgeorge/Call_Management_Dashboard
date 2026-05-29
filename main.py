from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.call_services import (
    create_call,
    get_all_calls,
    get_non_archived_calls,
    get_call_by_id,
    filter_calls,
    archive_all_calls,
    archive_call_by_id,
    unarchive_call_by_id,
    add_note_by_id,
    delete_call_by_id,
)
from src.core.exception_handlers import register_exception_handlers
from src.core.schemas import CallSchema, GetCallSchema, NoteSchema

app = FastAPI()
register_exception_handlers(app)


@app.post(
    "/calls",
    response_model=GetCallSchema,
    status_code=201,
    response_model_exclude_none=True,
)
async def create_call_endpoint(call: CallSchema, db: Session = Depends(get_db)):
    return create_call(db, call)


@app.get("/calls", response_model=list[GetCallSchema], response_model_exclude_none=True)
async def all_calls(db: Session = Depends(get_db)):
    return get_all_calls(db)


@app.get(
    "/calls/non-archived",
    response_model=list[GetCallSchema],
    response_model_exclude_none=True,
)
async def non_archived_calls(db: Session = Depends(get_db)):
    return get_non_archived_calls(db)


@app.get(
    "/calls/{call_id}", response_model=GetCallSchema, response_model_exclude_none=True
)
async def call_by_id(call_id: int, db: Session = Depends(get_db)):
    return get_call_by_id(db, call_id)


@app.get(
    "/calls/{call_filter}/filter",
    response_model=list[GetCallSchema],
    response_model_exclude_none=True,
)
async def filter_call(call_filter: str, db: Session = Depends(get_db)):
    return filter_calls(db, call_filter)


@app.patch("/calls/archive-all")
async def archive_all(db: Session = Depends(get_db)):
    return archive_all_calls(db)


@app.patch("/calls/{call_id}/archive")
async def archive(call_id: int, db: Session = Depends(get_db)):
    return archive_call_by_id(db, call_id)


@app.patch("/calls/{call_id}/unarchive")
async def unarchive(call_id: int, db: Session = Depends(get_db)):
    return unarchive_call_by_id(db, call_id)


@app.patch("/calls/{call_id}/notes")
async def add_note(call_id: int, note: NoteSchema, db: Session = Depends(get_db)):
    return add_note_by_id(db, call_id, note)


@app.delete("/calls/{call_id}")
async def delete(call_id: int, db: Session = Depends(get_db)):
    return delete_call_by_id(db, call_id)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
