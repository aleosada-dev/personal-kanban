from pydantic import BaseModel, Field, EmailStr
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
    board_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Board Schemas
class BoardBase(BaseModel):
    """Base board schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(default="#667eea", pattern="^#[0-9A-Fa-f]{6}$")


class BoardCreate(BoardBase):
    """Schema for creating a board"""
    is_default: bool = False


class BoardUpdate(BaseModel):
    """Schema for updating a board"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    is_default: Optional[bool] = None


class Board(BoardBase):
    """Schema for board response"""
    id: int
    user_id: int
    is_default: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BoardWithStats(Board):
    """Schema for board response with card statistics"""
    card_count: int = 0
    todo_count: int = 0
    in_progress_count: int = 0
    done_count: int = 0


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class User(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data"""
    username: Optional[str] = None
