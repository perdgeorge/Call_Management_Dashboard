from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.core.database import Base
from src.models.call import Call


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(), nullable=False)
    call_id: Mapped[int] = mapped_column(ForeignKey("calls.id"))
    call: Mapped["Call"] = relationship(back_populates="notes")
