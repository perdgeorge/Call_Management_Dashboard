from fastapi import FastAPI
from src.services.call_services import (
    get_all_calls,
    get_call_by_id,
    archive_call,
    unarchive_call,
    delete_call,
    filter_calls,
    add_note,
    get_non_archived_calls,
)

app = FastAPI()


@app.get("/All_Calls")
async def all_calls():
    return get_all_calls()


print(get_non_archived_calls())

print(get_call_by_id("3"))

print(
    add_note(
        "1",
        {
            "id": "note-1",
            "call_id": "1",
            "content": "Check my schedule for tomorrow",
        },
    )
)

print(archive_call("3"))

print(unarchive_call("10"))

print(filter_calls("not_archived"))

print(delete_call("1"))
