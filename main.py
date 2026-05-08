from src.services.call_services import (
    get_all_calls,
    get_call_by_id,
    archive_call,
)

print(get_all_calls())

print(get_call_by_id("3"))

print(archive_call("3"))
