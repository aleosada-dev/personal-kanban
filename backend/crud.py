from sqlalchemy.orm import Session
from typing import List, Optional

from backend import models, schemas


def get_cards(db: Session, skip: int = 0, limit: int = 100) -> List[models.Card]:
    """Get all cards"""
    return db.query(models.Card).order_by(
        models.Card.status,
        models.Card.priority.desc(),
        models.Card.created_at
    ).offset(skip).limit(limit).all()


def get_card(db: Session, card_id: int) -> Optional[models.Card]:
    """Get a specific card by ID"""
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def create_card(db: Session, card: schemas.CardCreate) -> models.Card:
    """Create a new card"""
    db_card = models.Card(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(db: Session, card_id: int, card: schemas.CardUpdate) -> Optional[models.Card]:
    """Update an existing card"""
    db_card = get_card(db, card_id)
    if db_card is None:
        return None

    update_data = card.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_card, field, value)

    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, card_id: int) -> bool:
    """Delete a card"""
    db_card = get_card(db, card_id)
    if db_card is None:
        return False

    db.delete(db_card)
    db.commit()
    return True
