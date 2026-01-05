from uuid import uuid4
from sqlalchemy import Boolean, Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    service = Column(String)
    completion_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # URL for the project's final / main image used in frontend cards
    main_image = Column(String, nullable=True)
    
    # relación con medios (imágenes y vídeos)
    media = relationship("ProjectMedia", back_populates="project")

class ProjectMedia(Base):
    __tablename__ = "project_media"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    file_url = Column(String)
    mime = Column(String)
    media_type = Column(String)  # 'image' or 'video'
    description = Column(Text, nullable=True)
    is_before = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="media")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, index=True)
    description = Column(Text)
    details = Column(Text)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    service = Column(String)
    message = Column(Text)
    status = Column(String, default="pending")  # pending, contacted, completed, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    number = Column(String, index=True)
    date = Column(DateTime)
    clientName = Column(String)
    clientAddress = Column(Text)
    clientDNI = Column(String, nullable=True)
    clientPhone = Column(String, nullable=True)
    clientEmail = Column(String, nullable=True)
    items = Column(JSON)
    taxRate = Column(String, nullable=True)
    validUntil = Column(DateTime, nullable=True)
    conditions = Column(Text, nullable=True)
    iban = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    number = Column(String, index=True)
    date = Column(DateTime)
    clientName = Column(String)
    clientAddress = Column(Text)
    clientDNI = Column(String, nullable=True)
    clientPhone = Column(String, nullable=True)
    clientEmail = Column(String, nullable=True)
    items = Column(JSON)
    taxRate = Column(String, nullable=True)
    iban = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)