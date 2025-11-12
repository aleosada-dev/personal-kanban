from sqlalchemy.orm import Session
from sqlalchemy import func
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

    # Create a default board for the new user
    default_board = models.Board(
        name="My Kanban Board",
        description="Default board",
        color="#667eea",
        is_default=True,
        user_id=db_user.id
    )
    db.add(default_board)
    db.commit()

    return db_user


# Board CRUD operations
def get_boards(db: Session, user_id: int) -> List[models.Board]:
    """Get all boards for a specific user"""
    return db.query(models.Board).filter(
        models.Board.user_id == user_id
    ).order_by(
        models.Board.is_default.desc(),
        models.Board.created_at
    ).all()


def get_board(db: Session, board_id: int, user_id: int) -> Optional[models.Board]:
    """Get a specific board by ID for a specific user"""
    return db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.user_id == user_id
    ).first()


def get_default_board(db: Session, user_id: int) -> Optional[models.Board]:
    """Get the default board for a user"""
    return db.query(models.Board).filter(
        models.Board.user_id == user_id,
        models.Board.is_default == True
    ).first()


def create_board(db: Session, board: schemas.BoardCreate, user_id: int) -> models.Board:
    """Create a new board for a specific user"""
    # If this board is marked as default, unset other default boards
    if board.is_default:
        db.query(models.Board).filter(
            models.Board.user_id == user_id,
            models.Board.is_default == True
        ).update({"is_default": False})

    db_board = models.Board(**board.model_dump(), user_id=user_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def update_board(db: Session, board_id: int, board: schemas.BoardUpdate, user_id: int) -> Optional[models.Board]:
    """Update an existing board for a specific user"""
    db_board = get_board(db, board_id, user_id)
    if db_board is None:
        return None

    update_data = board.model_dump(exclude_unset=True)

    # If this board is being set as default, unset other default boards
    if update_data.get("is_default") == True:
        db.query(models.Board).filter(
            models.Board.user_id == user_id,
            models.Board.is_default == True,
            models.Board.id != board_id
        ).update({"is_default": False})

    for field, value in update_data.items():
        setattr(db_board, field, value)

    db.commit()
    db.refresh(db_board)
    return db_board


def delete_board(db: Session, board_id: int, user_id: int) -> bool:
    """Delete a board for a specific user"""
    db_board = get_board(db, board_id, user_id)
    if db_board is None:
        return False

    # Don't allow deletion of the last board
    board_count = db.query(models.Board).filter(models.Board.user_id == user_id).count()
    if board_count <= 1:
        return False

    db.delete(db_board)
    db.commit()
    return True


def get_board_with_stats(db: Session, board_id: int, user_id: int) -> Optional[dict]:
    """Get board with card statistics"""
    board = get_board(db, board_id, user_id)
    if not board:
        return None

    cards = db.query(models.Card).filter(models.Card.board_id == board_id).all()

    return {
        **board.__dict__,
        "card_count": len(cards),
        "todo_count": sum(1 for c in cards if c.status == models.CardStatus.TODO),
        "in_progress_count": sum(1 for c in cards if c.status == models.CardStatus.IN_PROGRESS),
        "done_count": sum(1 for c in cards if c.status == models.CardStatus.DONE),
    }


# Card CRUD operations (updated to be board-specific)
def get_cards(db: Session, board_id: int, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Card]:
    """Get all cards for a specific board"""
    # Verify the board belongs to the user
    board = get_board(db, board_id, user_id)
    if not board:
        return []

    return db.query(models.Card).filter(
        models.Card.board_id == board_id
    ).order_by(
        models.Card.status,
        models.Card.priority.desc(),
        models.Card.created_at
    ).offset(skip).limit(limit).all()


def get_card(db: Session, card_id: int, user_id: int) -> Optional[models.Card]:
    """Get a specific card by ID, ensuring it belongs to the user"""
    # Join with board to verify ownership
    return db.query(models.Card).join(models.Board).filter(
        models.Card.id == card_id,
        models.Board.user_id == user_id
    ).first()


def create_card(db: Session, card: schemas.CardCreate, board_id: int, user_id: int) -> Optional[models.Card]:
    """Create a new card for a specific board"""
    # Verify the board belongs to the user
    board = get_board(db, board_id, user_id)
    if not board:
        return None

    db_card = models.Card(**card.model_dump(), board_id=board_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(db: Session, card_id: int, card: schemas.CardUpdate, user_id: int) -> Optional[models.Card]:
    """Update an existing card, ensuring it belongs to the user"""
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
    """Delete a card, ensuring it belongs to the user"""
    db_card = get_card(db, card_id, user_id)
    if db_card is None:
        return False

    db.delete(db_card)
    db.commit()
    return True
