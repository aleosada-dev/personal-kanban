from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum

from backend.database import Base


class CardStatus(str, enum.Enum):
    """Kanban card status enum"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Card(Base):
    """Kanban card model"""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(CardStatus),
        default=CardStatus.TODO,
        nullable=False,
        index=True
    )
    priority = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Card(id={self.id}, title='{self.title}', status='{self.status}')>"
