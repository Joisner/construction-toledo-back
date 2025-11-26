from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
router = APIRouter()
# NOTE: module-level debugger removed. Use a breakpoint inside endpoints to inspect request data.
@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Pause here when a login request arrives so you can inspect `form_data` in the debugger.

    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400, detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "is_admin": user.is_admin,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "access_token": security.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(models.User).filter(
        models.User.email == user_in.email
    ).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=security.get_password_hash(user_in.password),
        is_admin=user_in.is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user