"""
Suraksha — Verification Router
Endpoints for running the verification agent and viewing results.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.task import MAPTask
from services.verification_agent import run_verification, get_verification_summary

router = APIRouter(prefix="/api/verify", tags=["Verification"])


@router.post("/run")
async def trigger_verification(db: Session = Depends(get_db)):
    """
    Trigger the verification agent to scan mock logs
    and update task statuses.
    """
    results = run_verification(db)
    return {
        "message": "Verification scan complete",
        "results": results
    }


@router.get("/summary")
async def verification_summary(db: Session = Depends(get_db)):
    """Get overall verification/compliance summary."""
    summary = get_verification_summary(db)
    return summary


@router.get("/task/{task_id}")
async def task_verification_detail(task_id: int, db: Session = Depends(get_db)):
    """Get verification details and audit trail for a specific task."""
    task = db.query(MAPTask).filter(MAPTask.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    return {
        "task_ref": task.task_ref,
        "title": task.title,
        "status": task.status,
        "verified_at": task.verified_at.isoformat() if task.verified_at else None,
        "evidence_link": task.evidence_link,
        "audit_trail": task.get_audit_trail()
    }
