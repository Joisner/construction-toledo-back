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


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

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
    # URL of the project's final/main image used for cards in the frontend
    main_image: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    media: List[ProjectMedia] = []
    main_image: Optional[str] = None

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

# Public user shape for token responses: allow local emails like 'admin@localhost'
class TokenUser(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True


class TokenWithUser(BaseModel):
    access_token: str
    token_type: str
    user: TokenUser

class TokenPayload(BaseModel):
    sub: str
    exp: datetime


# Invoice / Budget related schemas
class InvoiceItem(BaseModel):
    description: str
    amount: float


class DocumentBase(BaseModel):
    number: str
    date: datetime
    clientName: str
    clientAddress: str
    clientDNI: Optional[str] = None
    clientPhone: Optional[str] = None
    clientEmail: Optional[EmailStr] = None
    items: List[InvoiceItem]
    taxRate: float
    iban: Optional[str] = None


class BudgetCreate(DocumentBase):
    validUntil: Optional[datetime] = None
    conditions: Optional[str] = None


class Budget(DocumentBase):
    id: str
    validUntil: Optional[datetime] = None
    conditions: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceCreate(DocumentBase):
    pass


class Invoice(DocumentBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True