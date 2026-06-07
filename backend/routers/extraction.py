"""
Suraksha — Extraction Router
Triggers LLM rule extraction and returns results.
"""

import json
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.circular import Circular
from models.rule import ExtractedRule
from models.task import MAPTask
from services.llm_extractor import extract_rules_from_text, validate_extraction
from services.pdf_parser import chunk_text
from services.map_generator import generate_maps_from_rules
from services.conflict_checker import check_conflicts, apply_conflict_flags

router = APIRouter(prefix="/api/extract", tags=["Extraction"])


@router.post("/{circular_id}")
async def extract_rules(circular_id: int, db: Session = Depends(get_db)):
    """
    Trigger LLM extraction pipeline for a circular.
    Extracts rules, generates MAPs, checks conflicts.
    """
    circular = db.query(Circular).filter(Circular.id == circular_id).first()
    if not circular:
        raise HTTPException(status_code=404, detail="Circular not found")

    if not circular.raw_text:
        raise HTTPException(status_code=400, detail="Circular has no extracted text")

    # Update status
    circular.status = "extracting"
    db.commit()

    try:
        # Step 1: Chunk text
        chunks = chunk_text(circular.raw_text)

        # Step 2: Extract rules via LLM
        extraction_result = await extract_rules_from_text(chunks, circular_id)

        # Step 3: Validate
        is_valid, message = validate_extraction(extraction_result)
        if not is_valid:
            raise HTTPException(status_code=422, detail=f"Invalid extraction: {message}")

        # Step 4: Save rules to DB
        saved_rules = []
        for rule_data in extraction_result["rules"]:
            deadline = None
            if rule_data.get("deadline"):
                try:
                    deadline = date.fromisoformat(rule_data["deadline"])
                except (ValueError, TypeError):
                    deadline = None

            rule = ExtractedRule(
                circular_id=circular_id,
                rule_id=rule_data["rule_id"],
                title=rule_data["title"],
                description=rule_data["description"],
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

        # Step 5: Check conflicts
        conflicts = await check_conflicts(extraction_result["rules"], db)
        if conflicts:
            apply_conflict_flags(db, saved_rules, conflicts)

        # Step 6: Generate MAP tasks
        tasks = generate_maps_from_rules(db, circular_id, saved_rules)

        # Update circular status
        circular.status = "processed"
        db.commit()

        return {
            "message": "Extraction complete",
            "circular_id": circular_id,
            "rules_extracted": len(saved_rules),
            "tasks_generated": len(tasks),
            "conflicts_found": len(conflicts),
            "rules": [r.to_dict() for r in saved_rules],
            "tasks": [t.to_dict() for t in tasks],
            "conflicts": conflicts
        }

    except HTTPException:
        raise
    except Exception as e:
        circular.status = "error"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


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
