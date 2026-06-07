"""
Suraksha — Tasks Router
CRUD operations for MAP tasks and dashboard statistics.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.task import MAPTask

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("")
async def list_tasks(
    department: str = Query(None, description="Filter by department"),
    status: str = Query(None, description="Filter by status"),
    priority: str = Query(None, description="Filter by priority"),
    circular_id: int = Query(None, description="Filter by circular"),
    db: Session = Depends(get_db)
):
    """List all MAP tasks with optional filters."""
    query = db.query(MAPTask)

    if department:
        query = query.filter(MAPTask.department == department)
    if status:
        query = query.filter(MAPTask.status == status)
    if priority:
        query = query.filter(MAPTask.priority == priority)
    if circular_id:
        query = query.filter(MAPTask.circular_id == circular_id)

    tasks = query.order_by(MAPTask.created_at.desc()).all()
    return {"tasks": [t.to_dict() for t in tasks]}


@router.get("/stats")
async def get_task_stats(db: Session = Depends(get_db)):
    """Get aggregate statistics for the dashboard."""
    all_tasks = db.query(MAPTask).all()

    if not all_tasks:
        return {
            "total": 0,
            "by_status": {},
            "by_department": {},
            "by_priority": {},
            "compliance_rate": 0
        }

    # Status breakdown
    by_status = {}
    for task in all_tasks:
        by_status[task.status] = by_status.get(task.status, 0) + 1

    # Department breakdown
    by_department = {}
    for task in all_tasks:
        dept = task.department or "Unassigned"
        if dept not in by_department:
            by_department[dept] = {"total": 0, "verified": 0, "pending": 0, "failed": 0}
        by_department[dept]["total"] += 1
        if task.status == "Verified":
            by_department[dept]["verified"] += 1
        elif task.status == "Pending":
            by_department[dept]["pending"] += 1
        elif task.status == "Failed":
            by_department[dept]["failed"] += 1

    # Priority breakdown
    by_priority = {}
    for task in all_tasks:
        prio = task.priority or "Medium"
        by_priority[prio] = by_priority.get(prio, 0) + 1

    # Compliance rate
    verified = sum(1 for t in all_tasks if t.status == "Verified")
    compliance_rate = round((verified / len(all_tasks)) * 100, 1) if all_tasks else 0

    # Effort summary
    total_effort = 0
    effort_by_dept = {}
    for task in all_tasks:
        if task.rule and task.rule.estimated_effort_days:
            effort = task.rule.estimated_effort_days
            total_effort += effort
            dept = task.department or "Unassigned"
            effort_by_dept[dept] = effort_by_dept.get(dept, 0) + effort

    return {
        "total": len(all_tasks),
        "by_status": by_status,
        "by_department": by_department,
        "by_priority": by_priority,
        "compliance_rate": compliance_rate,
        "total_effort_days": total_effort,
        "effort_by_department": effort_by_dept
    }


@router.get("/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task with its details."""
    task = db.query(MAPTask).filter(MAPTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@router.patch("/{task_id}")
async def update_task(task_id: int, updates: dict, db: Session = Depends(get_db)):
    """Update a task's status or other fields."""
    task = db.query(MAPTask).filter(MAPTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    allowed_fields = ["status", "owner", "priority"]
    for field, value in updates.items():
        if field in allowed_fields:
            setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task.to_dict()
