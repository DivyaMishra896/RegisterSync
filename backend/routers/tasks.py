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
    all_tasks = db.query(MAPTask).all()

    if not all_tasks:
        return {
            "total": 0,
            "by_status": {},
            "by_department": {},
            "by_priority": {},
            "compliance_rate": 0
        }

    by_status = {}
    for task in all_tasks:
        by_status[task.status] = by_status.get(task.status, 0) + 1

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

    by_priority = {}
    for task in all_tasks:
        prio = task.priority or "Medium"
        by_priority[prio] = by_priority.get(prio, 0) + 1

    verified = sum(1 for t in all_tasks if t.status == "Verified")
    compliance_rate = round((verified / len(all_tasks)) * 100, 1) if all_tasks else 0

    total_effort = 0
    effort_by_dept = {}
    for task in all_tasks:
        if task.rule and task.rule.estimated_effort_days:
            effort = task.rule.estimated_effort_days
            total_effort += effort
            dept = task.department or "Unassigned"
            effort_by_dept[dept] = effort_by_dept.get(dept, 0) + effort

    from models.rule import ExtractedRule
    unresolved_conflicts = db.query(ExtractedRule).filter(ExtractedRule.has_conflict == True).count()
    
    risk_score = 100
    for task in all_tasks:
        if task.status == "Failed":
            risk_score -= 15
        elif task.status == "Pending":
            if task.priority == "Critical":
                risk_score -= 10
            elif task.priority == "High":
                risk_score -= 5
            elif task.priority == "Medium":
                risk_score -= 2
                
    risk_score -= (unresolved_conflicts * 10)
    risk_score = max(0, min(100, risk_score)) 
    
    risk_level = "LOW RISK"
    if risk_score < 50:
        risk_level = "CRITICAL RISK"
    elif risk_score < 75:
        risk_level = "HIGH RISK"
    elif risk_score < 90:
        risk_level = "MEDIUM RISK"

    return {
        "total": len(all_tasks),
        "by_status": by_status,
        "by_department": by_department,
        "by_priority": by_priority,
        "compliance_rate": compliance_rate,
        "total_effort_days": total_effort,
        "effort_by_department": effort_by_dept,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "unresolved_conflicts": unresolved_conflicts
    }


@router.get("/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(MAPTask).filter(MAPTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@router.patch("/{task_id}")
async def update_task(task_id: int, updates: dict, db: Session = Depends(get_db)):
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
