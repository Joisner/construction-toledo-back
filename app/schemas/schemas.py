from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool

    class Config:
        from_attributes = True

# Project schemas
class ProjectMediaBase(BaseModel):
    file_url: str
    mime: Optional[str] = None
    media_type: str  # 'image' or 'video'
    description: Optional[str] = None
    is_before: Optional[bool] = None

class ProjectMediaCreate(ProjectMediaBase):
    pass

class ProjectMedia(ProjectMediaBase):
    id: str
    project_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    location: str
    service: str
    completion_date: datetime
    is_active: bool = True

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    media: List[ProjectMedia] = []

    class Config:
        from_attributes = True

# Service schemas
class ServiceBase(BaseModel):
    title: str
    description: str
    details: str
    image_url: Optional[str] = None
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Quote schemas
class QuoteBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service: str
    message: str

class QuoteCreate(QuoteBase):
    pass

class Quote(QuoteBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: datetime