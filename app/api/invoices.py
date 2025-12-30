from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Invoice)
def create_invoice(
    *,
    db: Session = Depends(get_db),
    invoice_in: schemas.InvoiceCreate,
) -> Any:
    """
    Create new invoice.
    """
    invoice_data = invoice_in.dict()
    invoice = models.Invoice(
        number=invoice_data.get('number'),
        date=invoice_data.get('date'),
        clientName=invoice_data.get('clientName'),
        clientAddress=invoice_data.get('clientAddress'),
        clientDNI=invoice_data.get('clientDNI'),
        clientPhone=invoice_data.get('clientPhone'),
        clientEmail=invoice_data.get('clientEmail'),
        items=invoice_data.get('items'),
        taxRate=str(invoice_data.get('taxRate')),
        iban=invoice_data.get('iban')
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/", response_model=List[schemas.Invoice])
def list_invoices(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve invoices (admin only).
    """
    invoices = db.query(models.Invoice).offset(skip).limit(limit).all()
    return invoices


@router.get("/{invoice_id}", response_model=schemas.Invoice)
def get_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    return {"status": "success"}
