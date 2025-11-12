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
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


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
