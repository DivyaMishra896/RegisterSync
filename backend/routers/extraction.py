"""
Suraksha — Extraction Router
Triggers LLM rule extraction and returns results. Supports SSE streaming.
"""

import json
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from database import get_db, SessionLocal
from models.circular import Circular
from models.rule import ExtractedRule
from models.task import MAPTask
from services.pdf_parser import chunk_text
from services.map_generator import generate_maps_from_rules
from services.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/api/extract", tags=["Extraction"])

@router.get("/{circular_id}/stream")
async def extract_rules_stream(circular_id: int):
    """
    Trigger LLM extraction pipeline for a circular and stream the reasoning via SSE.
    """
    async def event_generator():
        db = SessionLocal()
        try:
            circular = db.query(Circular).filter(Circular.id == circular_id).first()
            if not circular:
                yield {"event": "error", "data": "Circular not found"}
                return

            if not circular.raw_text:
                yield {"event": "error", "data": "Circular has no extracted text"}
                return

            circular.status = "extracting"
            db.commit()

            # 1. Chunk text
            chunks = chunk_text(circular.raw_text)

            # 2. Get existing rules for conflict check
            existing_rules_db = db.query(ExtractedRule).all()
            existing_rules = [
                {"rule_id": r.rule_id, "title": r.title, "description": r.description} 
                for r in existing_rules_db
            ]

            # 3. Run Orchestrator Pipeline
            orchestrator = OrchestratorAgent()
            final_data = None

            async for step in orchestrator.run_extraction_pipeline(chunks, circular_id, existing_rules):
                if step["type"] == "thought":
                    yield {
                        "event": "thought",
                        "data": json.dumps({"agent": step["agent"], "thought": step["thought"]})
                    }
                elif step["type"] == "final_result":
                    final_data = step["data"]

            # 4. Save results to DB
            rules_data = final_data.get("rules", [])
            conflicts_data = final_data.get("conflicts", [])

            saved_rules = []
            for rule_data in rules_data:
                deadline = None
                if rule_data.get("deadline"):
                    try:
                        deadline = date.fromisoformat(rule_data["deadline"])
                    except (ValueError, TypeError):
                        deadline = None

                rule = ExtractedRule(
                    circular_id=circular_id,
                    rule_id=rule_data.get("rule_id", "Unknown"),
                    title=rule_data.get("title", "Unknown"),
                    description=rule_data.get("description", ""),
                    affected_departments=json.dumps(rule_data.get("affected_departments", [])),
                    deadline=deadline,
                    priority=rule_data.get("priority", "Medium"),
                    estimated_effort_days=rule_data.get("estimated_effort_days", 7),
                )
                db.add(rule)
                saved_rules.append(rule)

            db.commit()
            for rule in saved_rules:
                db.refresh(rule)

            # Apply conflict flags
            if conflicts_data:
                conflict_map = {}
                for conflict in conflicts_data:
                    rule_id = conflict.get("new_rule_id")
                    if rule_id not in conflict_map:
                        conflict_map[rule_id] = []
                    conflict_map[rule_id].append(conflict)

                for rule in saved_rules:
                    if rule.rule_id in conflict_map:
                        rule.has_conflict = True
                        rule.conflict_details = json.dumps(conflict_map[rule.rule_id])
                db.commit()

            # Generate MAP tasks
            tasks = generate_maps_from_rules(db, circular_id, saved_rules)

            circular.status = "processed"
            db.commit()

            yield {
                "event": "complete",
                "data": json.dumps({
                    "rules_extracted": len(saved_rules),
                    "tasks_generated": len(tasks),
                    "conflicts_found": len(conflicts_data)
                })
            }

        except Exception as e:
            print(f"Streaming error: {e}")
            yield {"event": "error", "data": str(e)}
        finally:
            db.close()

    return EventSourceResponse(event_generator())


@router.get("/{circular_id}/rules")
async def get_rules(circular_id: int, db: Session = Depends(get_db)):
    """Get extracted rules for a circular."""
    rules = db.query(ExtractedRule).filter(
        ExtractedRule.circular_id == circular_id
    ).all()
    return {"rules": [r.to_dict() for r in rules]}


@router.get("/{circular_id}/conflicts")
async def get_conflicts(circular_id: int, db: Session = Depends(get_db)):
    """Get conflict details for rules in a circular."""
    rules = db.query(ExtractedRule).filter(
        ExtractedRule.circular_id == circular_id,
        ExtractedRule.has_conflict == True
    ).all()

    conflicts = []
    for rule in rules:
        if rule.conflict_details:
            conflict_data = json.loads(rule.conflict_details)
            conflicts.extend(conflict_data)

    return {"conflicts": conflicts}
