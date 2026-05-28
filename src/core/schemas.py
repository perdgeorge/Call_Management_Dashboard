from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import CallDirection, CallType


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NoteSchema(BaseSchema):
    content: str = Field(examples=["Follow up about billing"])


class GetNoteSchema(NoteSchema):
    id: int = Field(examples=[1])
    call_id: int = Field(examples=[1])


class CallSchema(BaseSchema):
    direction: CallDirection = Field(..., examples=["inbound"])
    from_number: str = Field(
        ...,
        pattern=r"^\+\d{2}\s\d{3}\s\d{7}$",
        max_length=15,
        examples=["+30 123 4567890"],
    )
    to_number: str = Field(
        ...,
        pattern=r"^\+\d{2}\s\d{3}\s\d{7}$",
        max_length=15,
        examples=["+30 098 7654321"],
    )
    call_type: CallType = Field(..., examples=["answered"])
    duration: int = Field(..., examples=[120])
    created_at: datetime = Field(..., examples=["2023-01-01T00:00:00"])
    is_archived: bool = Field(..., examples=[False])
    notes: List[NoteSchema] | None = Field(
        examples=[
            [
                {
                    "content": "Customer left a message about their invoice",
                }
            ]
        ],
        default=None,
    )


class GetCallSchema(CallSchema):
    id: int = Field(..., examples=[1])
    notes: List[GetNoteSchema] | None = None


class UpdateCallSchema(BaseSchema):
    is_archived: bool = Field(..., examples=[False])
    notes: List[NoteSchema] | None = Field(
        examples=[
            {
                "content": "Customer left a message about their invoice",
            }
        ],
        default=None,
    )
