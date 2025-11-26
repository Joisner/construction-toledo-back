from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Quote)
def create_quote(
    *,
    db: Session = Depends(get_db),
    quote_in: schemas.QuoteCreate,
) -> Any:
    """
    Create new quote request.
    """
    quote = models.Quote(**quote_in.dict())
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote

@router.get("/", response_model=List[schemas.Quote])
def get_quotes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve quotes.
    """
    quotes = db.query(models.Quote).offset(skip).limit(limit).all()
    return quotes

@router.put("/{quote_id}", response_model=schemas.Quote)
def update_quote(
    *,
    db: Session = Depends(get_db),
    quote_id: str,
    status: str,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update quote status.
    """
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    quote.status = status
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote

@router.delete("/{quote_id}")
def delete_quote(
    *,
    db: Session = Depends(get_db),
    quote_id: str,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete quote.
    """
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    db.delete(quote)
    db.commit()
    return {"status": "success"}