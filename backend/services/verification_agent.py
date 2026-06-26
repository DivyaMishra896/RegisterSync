import json
import os
from datetime import datetime
from sqlalchemy.orm import Session

from models.task import MAPTask
from config import settings


def load_mock_logs() -> dict:
    logs_dir = settings.MOCK_LOGS_DIR
    all_logs = {}

    for filename in os.listdir(logs_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, 'r') as f:
                entries = json.load(f)
                for entry in entries:
                    task_ref = entry.get("task_ref")
                    if task_ref:
                        all_logs[task_ref] = entry

    return all_logs


def run_verification(db: Session) -> dict:
    logs = load_mock_logs()

    pending_tasks = db.query(MAPTask).filter(
        MAPTask.status.in_(["Pending", "In Progress"])
    ).all()

    results = {
        "total_checked": len(pending_tasks),
        "verified": 0,
        "failed": 0,
        "partially_done": 0,
        "no_evidence": 0,
        "details": []
    }

    for task in pending_tasks:
        log_entry = logs.get(task.task_ref)

        if log_entry:
            log_status = log_entry.get("status", "").lower()
            timestamp = log_entry.get("timestamp", datetime.utcnow().isoformat())
            evidence = log_entry.get("evidence", "")
            action = log_entry.get("action", "")

            if log_status == "completed":
                task.status = "Verified"
                task.verified_at = datetime.utcnow()
                task.evidence_link = evidence
                task.add_audit_event({
                    "event": "Auto-verified by Suraksha Agent",
                    "timestamp": timestamp,
                    "action_found": action,
                    "evidence": evidence,
                    "source_log": log_entry.get("source_log", "system"),
                    "auto": True
                })
                results["verified"] += 1

            elif log_status == "partial":
                task.status = "Partially Done"
                task.add_audit_event({
                    "event": "Partial completion detected by Suraksha Agent",
                    "timestamp": timestamp,
                    "action_found": action,
                    "evidence": evidence,
                    "notes": log_entry.get("notes", "Some sub-tasks remain incomplete"),
                    "auto": True
                })
                results["partially_done"] += 1

            elif log_status == "failed":
                task.status = "Failed"
                task.add_audit_event({
                    "event": "Task failure detected by Suraksha Agent",
                    "timestamp": timestamp,
                    "action_found": action,
                    "reason": log_entry.get("reason", "Implementation not found in logs"),
                    "auto": True
                })
                results["failed"] += 1

            result_detail = {
                "task_ref": task.task_ref,
                "title": task.title,
                "previous_status": "Pending",
                "new_status": task.status,
                "evidence": evidence,
                "timestamp": timestamp
            }
            results["details"].append(result_detail)

        else:
            results["no_evidence"] += 1
            results["details"].append({
                "task_ref": task.task_ref,
                "title": task.title,
                "previous_status": "Pending",
                "new_status": "Pending",
                "evidence": None,
                "note": "No log evidence found — task remains pending"
            })

    db.commit()
    return results


def get_verification_summary(db: Session) -> dict:
    all_tasks = db.query(MAPTask).all()

    summary = {
        "total_tasks": len(all_tasks),
        "verified": sum(1 for t in all_tasks if t.status == "Verified"),
        "pending": sum(1 for t in all_tasks if t.status == "Pending"),
        "failed": sum(1 for t in all_tasks if t.status == "Failed"),
        "partially_done": sum(1 for t in all_tasks if t.status == "Partially Done"),
        "in_progress": sum(1 for t in all_tasks if t.status == "In Progress"),
    }

    if summary["total_tasks"] > 0:
        summary["compliance_rate"] = round(
            (summary["verified"] / summary["total_tasks"]) * 100, 1
        )
    else:
        summary["compliance_rate"] = 0

    return summary
