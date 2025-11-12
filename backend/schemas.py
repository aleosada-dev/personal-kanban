from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from backend.models import CardStatus


class CardBase(BaseModel):
    """Base card schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: CardStatus = CardStatus.TODO
    priority: int = Field(default=0, ge=0)


class CardCreate(CardBase):
    """Schema for creating a card"""
    pass


class CardUpdate(BaseModel):
    """Schema for updating a card"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[CardStatus] = None
    priority: Optional[int] = Field(None, ge=0)


class Card(CardBase):
    """Schema for card response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
