from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NoteSchema(BaseSchema):
    content: str = Field(examples="Follow up about billing")


class GetNoteSchema(NoteSchema):
    id: int = Field(examples=1)
    call_id: int = Field(examples=1)


class CreateNoteSchema(NoteSchema):
    pass
