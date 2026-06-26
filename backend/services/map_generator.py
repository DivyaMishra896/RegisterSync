import json
from datetime import datetime
from sqlalchemy.orm import Session

from models.rule import ExtractedRule
from models.task import MAPTask
from services.department_router import CircularAssigner
from services.department_data import get_default_owner


def generate_maps_from_rules(db: Session, circular_id: int, rules: list[ExtractedRule]) -> list[MAPTask]:
    tasks = []
    task_counter = 1

    for rule in rules:
        combined_text = f"{rule.title} {rule.description}"
        assignment = CircularAssigner.assign(combined_text)

        dept = assignment["department"]
        task_ref = f"MAP-{task_counter:03d}"

        task_title, task_desc = _create_task_details(rule, dept)

        task = MAPTask(
            rule_id=rule.id,
            circular_id=circular_id,
            task_ref=task_ref,
            title=task_title,
            description=task_desc,
            department=dept,
            priority=rule.priority,
            deadline=rule.deadline,
            status="Pending",
            owner=get_default_owner(dept),
            sub_vertical=assignment.get("sub_vertical", "") or "",
            regulator=assignment.get("regulator", "") or "",
            advisory=assignment.get("advisory", "") or "",
            routing_reason=assignment.get("routing_reason", "") or "",
            audit_trail=json.dumps([{
                "event": "Task created from rule extraction",
                "timestamp": datetime.utcnow().isoformat(),
                "rule_ref": rule.rule_id,
                "assigned_department": dept,
                "assignment_method": "hybrid_keyword_roundrobin",
                "auto": True
            }])
        )

        db.add(task)
        tasks.append(task)
        task_counter += 1

    db.commit()

    for task in tasks:
        db.refresh(task)

    return tasks


def _create_task_details(rule: ExtractedRule, department: str) -> tuple[str, str]:
    title = f"[{department}] {rule.title}"

    description = (
        f"**Source Rule**: {rule.rule_id}\n\n"
        f"**Requirement**: {rule.description}\n\n"
        f"**Action Required**: Implement compliance measures for this requirement "
        f"within the {department} department.\n\n"
        f"**Estimated Effort**: {rule.estimated_effort_days} days\n\n"
        f"**Priority**: {rule.priority}"
    )

    return title, description
