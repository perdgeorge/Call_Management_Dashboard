from faker import Faker
from src.core.schemas import CallSchema, GetNoteSchema
from src.core.enums import CallDirection, CallType

fake = Faker()


def make_note_payload() -> GetNoteSchema:
    data = {
        "id": fake.random_int(min=1, max=100),
        "content": fake.sentence(),
        "call_id": fake.random_int(min=1, max=100),
    }
    return GetNoteSchema(**data)


def make_call_payload() -> CallSchema:
    mock_notes = [make_note_payload()]
    data = {
        "direction": CallDirection.INBOUND.value,
        "from_number": fake.numerify("+30 69# #######"),
        "to_number": fake.numerify("+30 69# #######"),
        "call_type": CallType.ANSWERED.value,
        "duration": fake.random_int(min=10, max=120),
        "is_archived": False,
        "notes": mock_notes,
    }
    return CallSchema(**data)
