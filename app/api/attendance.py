from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import models
from app.schemas import schemas
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Attendance])
def list_attendance(
    db: Session = Depends(get_db),
    date: str | None = None,
    worker_id: int | None = None,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    query = db.query(models.AttendanceRecord)
    if date:
        query = query.filter(models.AttendanceRecord.date == date)
    if worker_id is not None:
        query = query.filter(models.AttendanceRecord.worker_id == worker_id)
    records = query.order_by(models.AttendanceRecord.id.desc()).all()
    return records

@router.post("/", response_model=schemas.Attendance)
def create_attendance(
    *,
    db: Session = Depends(get_db),
    attendance_in: schemas.AttendanceCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    record = models.AttendanceRecord(
        worker_id=attendance_in.worker_id,
        worker_name=attendance_in.worker_name,
        type=attendance_in.type,
        time=attendance_in.timestamp[11:16] if len(attendance_in.timestamp) >= 16 else "",
        date=attendance_in.timestamp[0:10] if len(attendance_in.timestamp) >= 10 else "",
        date_iso=attendance_in.timestamp[0:10] if len(attendance_in.timestamp) >= 10 else "",
        photo=attendance_in.photo,
        timestamp=attendance_in.timestamp,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}/")
def delete_attendance(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    record = db.query(models.AttendanceRecord).filter(models.AttendanceRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(record)
    db.commit()
    return {"status": "success"}
