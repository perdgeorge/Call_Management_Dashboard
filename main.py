from fastapi import FastAPI
from src.services.call_services import (
    get_all_calls,
    get_non_archived_calls,
    get_call_by_id,
    archive_call_by_id,
    unarchive_call_by_id,
    delete_call_by_id,
    filter_calls,
    add_note_by_id,
    archive_all_calls,
)
from src.core.exception_handlers import register_exception_handlers
from src.core.schemas import (
    GetCallSchema,
    CreateNoteSchema,
)

app = FastAPI()
register_exception_handlers(app)


@app.get("/calls", response_model=list[GetCallSchema], response_model_exclude_none=True)
async def all_calls():
    return get_all_calls()


@app.get(
    "/calls/non-archived",
    response_model=list[GetCallSchema],
    response_model_exclude_none=True,
)
async def non_archived_calls():
    return get_non_archived_calls()


@app.get(
    "/calls/{call_id}", response_model=GetCallSchema, response_model_exclude_none=True
)
async def call_by_id(call_id: int):
    return get_call_by_id(call_id)


@app.get(
    "/calls/{call_filter}/filter",
    response_model=list[GetCallSchema],
    response_model_exclude_none=True,
)
async def filter_call(call_filter: str):
    return filter_calls(call_filter)


@app.patch("/calls/archive-all")
async def archive_all():
    return archive_all_calls()


@app.patch("/calls/{call_id}/archive")
async def archive(call_id: int):
    return archive_call_by_id(call_id)


@app.patch("/calls/{call_id}/unarchive")
async def unarchive(call_id: int):
    return unarchive_call_by_id(call_id)


@app.patch("/calls/{call_id}/notes")
async def add_note(call_id: int, note: CreateNoteSchema):
    return add_note_by_id(call_id, note)


@app.delete("/calls/{call_id}")
async def delete(call_id: int):
    return delete_call_by_id(call_id)


@app.get("/health")
async def health_check():
    return {"200": "OK"}
