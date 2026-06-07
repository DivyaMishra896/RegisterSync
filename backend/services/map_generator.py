"""
Suraksha — MAP Generator Service
Converts extracted rules into Measurable Action Points (MAPs).
Each rule generates one or more actionable tasks.
"""

import json
from datetime import datetime
from sqlalchemy.orm import Session

from models.rule import ExtractedRule
from models.task import MAPTask
from services.department_router import route_to_department


def generate_maps_from_rules(db: Session, circular_id: int, rules: list[ExtractedRule]) -> list[MAPTask]:
    """
    Generate MAP tasks from extracted rules.
    Each rule becomes one primary task, routed to the appropriate department.
    """
    tasks = []
    task_counter = 1

    for rule in rules:
        departments = rule.get_departments()

        # Generate a task for each affected department
        for dept in departments:
            task_ref = f"MAP-{task_counter:03d}"

            # Generate actionable task title and description
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
                owner=_assign_default_owner(dept),
                audit_trail=json.dumps([{
                    "event": "Task created from rule extraction",
                    "timestamp": datetime.utcnow().isoformat(),
                    "rule_ref": rule.rule_id,
                    "auto": True
                }])
            )

            db.add(task)
            tasks.append(task)
            task_counter += 1

    db.commit()

    # Refresh to get IDs
    for task in tasks:
        db.refresh(task)

    return tasks


def _create_task_details(rule: ExtractedRule, department: str) -> tuple[str, str]:
    """Generate actionable task title and description from rule and department."""
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


def _assign_default_owner(department: str) -> str:
    """Assign a default owner based on department."""
    owners = {
        "IT Security": "CISO Office",
        "Risk Management": "Chief Risk Officer",
        "Operations": "Head of Operations",
    }
    return owners.get(department, "Compliance Team")
