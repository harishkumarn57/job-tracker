from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("", response_model=schemas.JobOut, status_code=201)
def create_job(data: schemas.JobCreate, db: Session = Depends(get_db)):
    job = models.Job(**data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=list[schemas.JobOut])
def list_jobs(
    status: schemas.Status | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Job)
    if status:
        query = query.filter(models.Job.status == status)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Job.company.ilike(pattern),
                models.Job.role.ilike(pattern),
            )
        )
    return query.all()


@router.get("/stats")
def job_stats(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Job.status, func.count(models.Job.id))
        .group_by(models.Job.status)
        .all()
    )
    counts = {status: count for status, count in rows}
    by_status = {
        s: counts.get(s, 0)
        for s in ["Applied", "Interview", "Offer", "Rejected"]
    }
    return {"total": sum(by_status.values()), "by_status": by_status}


@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=schemas.JobOut)
def update_job(job_id: int, data: schemas.JobUpdate, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()