from dataclasses import dataclass, field
from datetime import datetime
from src.core.enums import CallDirection, CallType
from pydantic import BaseModel


@dataclass
class Note(BaseModel):
    id: str
    content: str


@dataclass
class Call(BaseModel):
    id: int
    direction: CallDirection
    from_number: str
    to_number: str
    call_type: CallType
    duration: int
    is_archived: bool
    created_at: datetime
    notes: list[Note] = field(default_factory=list)
