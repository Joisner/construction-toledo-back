from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Service])
def get_services(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve services.
    """
    services = db.query(models.Service).offset(skip).limit(limit).all()
    return services

@router.post("/", response_model=schemas.Service)
def create_service(
    *,
    db: Session = Depends(get_db),
    service_in: schemas.ServiceCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new service.
    """
    service = models.Service(**service_in.dict())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@router.put("/{service_id}", response_model=schemas.Service)
def update_service(
    *,
    db: Session = Depends(get_db),
    service_id: str,
    service_in: schemas.ServiceCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update service.
    """
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    for field, value in service_in.dict().items():
        setattr(service, field, value)
    
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@router.delete("/{service_id}")
def delete_service(
    *,
    db: Session = Depends(get_db),
    service_id: str,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete service.
    """
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(service)
    db.commit()
    return {"status": "success"}