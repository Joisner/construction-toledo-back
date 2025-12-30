from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Budget)
def create_budget(
    *,
    db: Session = Depends(get_db),
    budget_in: schemas.BudgetCreate,
) -> Any:
    """
    Create new budget (presupuesto).
    """
    # convert pydantic items -> Python native (JSON serializable)
    budget_data = budget_in.dict()
    budget = models.Budget(
        number=budget_data.get('number'),
        date=budget_data.get('date'),
        clientName=budget_data.get('clientName'),
        clientAddress=budget_data.get('clientAddress'),
        clientDNI=budget_data.get('clientDNI'),
        clientPhone=budget_data.get('clientPhone'),
        clientEmail=budget_data.get('clientEmail'),
        items=budget_data.get('items'),
        taxRate=str(budget_data.get('taxRate')),
        validUntil=budget_data.get('validUntil'),
        conditions=budget_data.get('conditions'),
        iban=budget_data.get('iban')
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/", response_model=List[schemas.Budget])
def list_budgets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve budgets (admin only).
    """
    budgets = db.query(models.Budget).offset(skip).limit(limit).all()
    return budgets


@router.get("/{budget_id}", response_model=schemas.Budget)
def get_budget(
    budget_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(budget)
    db.commit()
    return {"status": "success"}
