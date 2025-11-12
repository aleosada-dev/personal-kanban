from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from backend import models, schemas, crud
from backend.database import engine, get_db
from backend.auth import (
    get_current_active_user,
    verify_password,
    create_access_token,
    get_password_hash
)
from backend.config import get_settings

settings = get_settings()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Kanban Board")

# Add CORS middleware for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/")
async def home(request: Request):
    """Render the login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/board")
async def board(request: Request):
    """Render the main kanban board page (protected)"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register")
async def register_page(request: Request):
    """Render the registration page"""
    return templates.TemplateResponse("register.html", {"request": request})


# Authentication Endpoints
@app.post("/api/auth/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    return crud.create_user(db, user)


@app.post("/api/auth/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    # Get user by username
    user = crud.get_user_by_username(db, user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=schemas.User)
async def get_me(current_user: models.User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


# API Endpoints for Cards (Protected)
@app.get("/api/cards", response_model=List[schemas.Card])
def get_cards(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all kanban cards for the current user"""
    cards = crud.get_cards(db, current_user.id)
    return cards


@app.post("/api/cards", response_model=schemas.Card, status_code=status.HTTP_201_CREATED)
def create_card(
    card: schemas.CardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new kanban card for the current user"""
    return crud.create_card(db, card, current_user.id)


@app.put("/api/cards/{card_id}", response_model=schemas.Card)
def update_card(
    card_id: int,
    card: schemas.CardUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a kanban card for the current user"""
    db_card = crud.update_card(db, card_id, card, current_user.id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card


@app.delete("/api/cards/{card_id}")
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a kanban card for the current user"""
    success = crud.delete_card(db, card_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully"}


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
