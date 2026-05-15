from fastapi import FastAPI
from src.models.call import Note
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

app = FastAPI()


@app.get("/Calls")
async def all_calls():
    return get_all_calls()


@app.get("/Non_Archived_Calls")
async def non_archived_calls():
    return get_non_archived_calls()


@app.get("/{call_id}")
async def call_by_id(call_id: str):
    return get_call_by_id(call_id)


@app.get("/Calls/{call_filter}/Filter")
async def filter_call(call_filter: str):
    return filter_calls(call_filter)


@app.patch("/Calls/{call_id}/Archive")
async def archive(call_id: str):
    return archive_call_by_id(call_id)


@app.patch("/Calls/{call_id}/Unarchive")
async def unarchive(call_id: str):
    return unarchive_call_by_id(call_id)


@app.patch("/Calls/{call_id}/Note")
async def add_note(call_id: str, note: Note):
    return add_note_by_id(call_id, note)


@app.delete("/Calls/{call_id}")
async def delete(call_id: str):
    return delete_call_by_id(call_id)
