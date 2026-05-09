from datetime import datetime


class Note:
    id: str
    call_id: int
    content: str


class Call:
    id: int
    direction: str
    from_number: str
    to_number: str
    call_type: str
    duration: int
    is_archived: bool
    created_at: datetime
    notes: list[Note]
