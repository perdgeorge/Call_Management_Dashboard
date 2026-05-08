from src.services.call_services import (
    get_all_calls,
    get_call_by_id,
    archive_call,
    unarchive_call,
    delete_call,
)

print(get_all_calls())

print(get_call_by_id("3"))

print(archive_call("3"))

print(unarchive_call("10"))

print(delete_call("1"))
