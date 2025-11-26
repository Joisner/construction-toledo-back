from datetime import datetime
from typing import Any, List, Optional
import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api import deps

UPLOAD_DIR = os.path.abspath(os.path.join(os.getcwd(), "uploads", "projects"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.get("/", response_model=List[schemas.Project])
def get_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve projects.
    """
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=schemas.Project)
def get_project_by_id(
    *,
    project_id: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get project by ID.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project    

@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: schemas.ProjectCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new project.
    """
    project = models.Project(**project_in.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}/media", response_model=schemas.ProjectMedia)
def upload_project_media(
    *,
    project_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    is_before: Optional[bool] = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Upload an image or video for a project. Stores file in `uploads/projects/{project_id}` and
    creates a ProjectMedia record.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Validate file (mime + size)
    validate_file(file)

    # Save file to disk
    project_dir = os.path.join(UPLOAD_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(project_dir, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Determine media type from content type
    content_type = file.content_type or "application/octet-stream"
    media_type = "image" if content_type.startswith("image/") else "video" if content_type.startswith("video/") else "file"

    media = models.ProjectMedia(
        id=uuid4().hex,
        project_id=project_id,
        file_url=f"/uploads/projects/{project_id}/{filename}",
        mime=content_type,
        media_type=media_type,
        description=description,
        is_before=is_before,
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


def validate_file(file: UploadFile) -> None:
    """Validate mime type and size according to settings."""
    content_type = file.content_type or "application/octet-stream"
    allowed = settings.UPLOAD_ALLOWED_MIMES
    if content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"File type {content_type} is not allowed")

    # attempt to determine file size
    try:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)
    except Exception:
        # if we can't determine size, reject to be safe
        raise HTTPException(status_code=400, detail="Could not determine file size")

    max_bytes = settings.UPLOAD_MAX_SIZE_MB * 1024 * 1024
    if size > max_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Max {settings.UPLOAD_MAX_SIZE_MB} MB allowed")


@router.post("/{project_id}/media/batch", response_model=List[schemas.ProjectMedia])
def upload_project_media_batch(
    *,
    project_id: str,
    files: List[UploadFile] = File(...),
    description: Optional[str] = Form(None),
    is_before: Optional[bool] = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Upload multiple images/videos for a project in a single request.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_dir = os.path.join(UPLOAD_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)

    medias: List[models.ProjectMedia] = []
    for file in files:
        validate_file(file)
        filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(project_dir, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        content_type = file.content_type or "application/octet-stream"
        media_type = "image" if content_type.startswith("image/") else "video" if content_type.startswith("video/") else "file"

        media = models.ProjectMedia(
            id=uuid4().hex,
            project_id=project_id,
            file_url=f"/uploads/projects/{project_id}/{filename}",
            mime=content_type,
            media_type=media_type,
            description=description,
            is_before=is_before,
        )
        db.add(media)
        medias.append(media)

    db.commit()
    for m in medias:
        db.refresh(m)
    return medias


@router.delete("/{project_id}/media/{media_id}")
def delete_project_media(
    *,
    project_id: str,
    media_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a project's media record and remove the file from disk.
    """
    media = db.query(models.ProjectMedia).filter(models.ProjectMedia.id == media_id).first()
    if not media or media.project_id != project_id:
        raise HTTPException(status_code=404, detail="Media not found")

    # remove physical file
    try:
        filename = os.path.basename(media.file_url)
        project_dir = os.path.join(UPLOAD_DIR, project_id)
        file_path = os.path.join(project_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        # log? for now ignore file deletion errors
        pass

    db.delete(media)
    db.commit()
    return {"status": "deleted"}

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: str,
    project_in: schemas.ProjectCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update project.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for field, value in project_in.dict().items():
        setattr(project, field, value)
    
    project.updated_at = datetime.utcnow()
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete project.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"status": "success"}