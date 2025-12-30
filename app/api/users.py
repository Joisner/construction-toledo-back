from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api import deps
from app.core import security

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def list_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve users (admin only).
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=schemas.User)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a single user. Allowed for admin or the user themself.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not (current_user.is_admin or current_user.id == user_id):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: str,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a user. Allowed for admin or the user themself.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not (current_user.is_admin or current_user.id == user_id):
        raise HTTPException(status_code=403, detail="Not enough privileges")

    data = user_in.dict(exclude_unset=True)
    # handle password separately
    if 'password' in data:
        user.hashed_password = security.get_password_hash(data.pop('password'))

    # if email change, ensure uniqueness
    if 'email' in data:
        existing = db.query(models.User).filter(models.User.email == data['email']).first()
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already in use")

    for field, value in data.items():
        if hasattr(user, field):
            setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a user (admin only).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "success"}
