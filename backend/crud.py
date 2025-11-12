from sqlalchemy.orm import Session
from typing import List, Optional

from backend import models, schemas
from backend.auth import get_password_hash


# User CRUD operations
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Card CRUD operations (updated to be user-specific)
def get_cards(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Card]:
    """Get all cards for a specific user"""
    return db.query(models.Card).filter(
        models.Card.user_id == user_id
    ).order_by(
        models.Card.status,
        models.Card.priority.desc(),
        models.Card.created_at
    ).offset(skip).limit(limit).all()


def get_card(db: Session, card_id: int, user_id: int) -> Optional[models.Card]:
    """Get a specific card by ID for a specific user"""
    return db.query(models.Card).filter(
        models.Card.id == card_id,
        models.Card.user_id == user_id
    ).first()


def create_card(db: Session, card: schemas.CardCreate, user_id: int) -> models.Card:
    """Create a new card for a specific user"""
    db_card = models.Card(**card.model_dump(), user_id=user_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(db: Session, card_id: int, card: schemas.CardUpdate, user_id: int) -> Optional[models.Card]:
    """Update an existing card for a specific user"""
    db_card = get_card(db, card_id, user_id)
    if db_card is None:
        return None

    update_data = card.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_card, field, value)

    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, card_id: int, user_id: int) -> bool:
    """Delete a card for a specific user"""
    db_card = get_card(db, card_id, user_id)
    if db_card is None:
        return False

    db.delete(db_card)
    db.commit()
    return True
