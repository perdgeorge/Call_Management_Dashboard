from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Enum, func

from src.core.enums import CallDirection, CallType
from src.core.database import Base
from src.models.note import Note


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction: Mapped[CallDirection] = mapped_column(
        Enum(CallDirection), nullable=False
    )
    from_number: Mapped[str] = mapped_column(String(15), nullable=False)
    to_number: Mapped[str] = mapped_column(String(15), nullable=False)
    call_type: Mapped[CallType] = mapped_column(Enum(CallType), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    notes: Mapped[list[Note]] = relationship(back_populates="call")
