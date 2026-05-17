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
)
from src.core.exception_handlers import register_exception_handlers
from src.core.schemas import (
    GetCallSchema,
    CreateNoteSchema,
    DeleteCallSchema,
)

app = FastAPI()
register_exception_handlers(app)


@app.get("/Calls", response_model=list[GetCallSchema])
async def all_calls():
    return get_all_calls()


@app.get("/Non_Archived_Calls", response_model=list[GetCallSchema])
async def non_archived_calls():
    return get_non_archived_calls()


@app.get("/Calls/{call_id}", response_model=GetCallSchema)
async def call_by_id(call_id: int):
    return get_call_by_id(call_id)


@app.get("/Calls/{call_filter}/Filter", response_model=list[GetCallSchema])
async def filter_call(call_filter: str):
    return filter_calls(call_filter)


@app.patch("/Calls/{call_id}/Archive")
async def archive(call_id: int):
    return archive_call_by_id(call_id)


@app.patch("/Calls/{call_id}/Unarchive")
async def unarchive(call_id: int):
    return unarchive_call_by_id(call_id)


@app.patch("/Calls/{call_id}/Note")
async def add_note(call_id: int, note: CreateNoteSchema):
    return add_note_by_id(call_id, note)


@app.delete("/Calls/{call_id}", response_model=DeleteCallSchema)
async def delete(call_id: int):
    return delete_call_by_id(call_id)


@app.get("/health")
async def health_check():
    return {"200": "OK"}
