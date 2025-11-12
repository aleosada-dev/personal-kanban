from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from backend import models, schemas, crud
from backend.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Kanban Board")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/")
async def home(request: Request):
    """Render the main kanban board page"""
    return templates.TemplateResponse("index.html", {"request": request})


# API Endpoints for Cards
@app.get("/api/cards", response_model=List[schemas.Card])
def get_cards(db: Session = Depends(get_db)):
    """Get all kanban cards"""
    cards = crud.get_cards(db)
    return cards


@app.post("/api/cards", response_model=schemas.Card)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    """Create a new kanban card"""
    return crud.create_card(db, card)


@app.put("/api/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, card: schemas.CardUpdate, db: Session = Depends(get_db)):
    """Update a kanban card"""
    db_card = crud.update_card(db, card_id, card)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card


@app.delete("/api/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    """Delete a kanban card"""
    success = crud.delete_card(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully"}


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
