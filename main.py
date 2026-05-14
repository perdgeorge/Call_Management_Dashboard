from fastapi import FastAPI
from src.services.call_services import (
    get_all_calls,
    get_non_archived_calls,
    get_call_by_id,
    archive_call,
    unarchive_call,
    delete_call,
    filter_calls,
    add_note,
)

app = FastAPI()


@app.get("/All_Calls")
async def all_calls():
    return get_all_calls()


@app.get("/Non_Archived_Calls")
async def non_archived_calls():
    return get_non_archived_calls()


@app.get("/{call_id}")
async def call_by_id(call_id: str):
    return get_call_by_id(call_id)


@app.get("/Filter_Calls/{call_filter}")
async def filter_call(call_filter: str):
    return filter_calls(call_filter)


@app.patch("/Archive_Call/{call_id}")
async def archive(call_id: str):
    return archive_call(call_id)


@app.patch("/Unarchive_Call/{call_id}")
async def unarchive(call_id: str):
    return unarchive_call(call_id)


@app.delete("/Delete_Call/{call_id}")
async def delete(call_id: str):
    return delete_call(call_id)
