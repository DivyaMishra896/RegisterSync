"""
Suraksha — Conflict Checker Service
Detects conflicts between new rules and existing rules in the database.
Uses semantic comparison to flag contradictions.
"""

import json
import asyncio
from sqlalchemy.orm import Session
from models.rule import ExtractedRule
from config import settings


# Pre-built conflict scenario for demo (old rule from a "2022 circular")
MOCK_EXISTING_RULES = [
    {
        "rule_id": "HIST-001",
        "title": "Quarterly VAPT Assessment Schedule",
        "description": "Banks shall conduct VAPT assessments on a quarterly basis (every 3 months) for all critical information systems.",
        "source": "RBI Circular 2022/14",
        "deadline": "2022-12-31"
    },
    {
        "rule_id": "HIST-002",
        "title": "Data Storage Flexibility for Payment Systems",
        "description": "Regulated entities may store payment system data in approved overseas data centers provided adequate security measures and bilateral agreements are in place.",
        "source": "RBI Circular 2021/08",
        "deadline": "2022-06-30"
    }
]

# Pre-built conflict results for demo
MOCK_CONFLICT_RESULTS = [
    {
        "new_rule_id": "R-001",
        "new_rule_title": "Mandatory VAPT Assessment for Core Banking Systems",
        "existing_rule_id": "HIST-001",
        "existing_rule_title": "Quarterly VAPT Assessment Schedule",
        "existing_source": "RBI Circular 2022/14",
        "conflict_type": "SUPERSEDED",
        "severity": "Medium",
        "reason": "The new circular changes VAPT frequency from quarterly (every 3 months) to semi-annual (every 6 months). This relaxes the previous requirement. Banks currently on quarterly schedules should verify if the semi-annual timeline is now the minimum standard or if quarterly remains recommended."
    },
    {
        "new_rule_id": "R-005",
        "new_rule_title": "Data Localization and Cross-Border Data Transfer",
        "existing_rule_id": "HIST-002",
        "existing_rule_title": "Data Storage Flexibility for Payment Systems",
        "existing_source": "RBI Circular 2021/08",
        "conflict_type": "CONTRADICTS",
        "severity": "High",
        "reason": "The new circular mandates that ALL payment system data must be stored exclusively within India, directly contradicting the 2021 circular that permitted overseas storage with adequate security. Banks with overseas data centers must now plan full migration within 6 months."
    }
]


async def check_conflicts(new_rules: list[dict], db: Session) -> list[dict]:
    """
    Check for conflicts between new rules and existing rules.

    Args:
        new_rules: List of newly extracted rule dictionaries
        db: Database session

    Returns:
        List of conflict reports
    """
    if settings.LLM_MODE == "mock":
        await asyncio.sleep(1.5)  # Simulate processing
        return MOCK_CONFLICT_RESULTS

    # Live mode: compare against existing rules in DB
    existing_rules = db.query(ExtractedRule).all()

    if not existing_rules:
        return []

    # Use Claude for semantic comparison
    try:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        existing_json = json.dumps([{
            "rule_id": r.rule_id,
            "title": r.title,
            "description": r.description
        } for r in existing_rules])

        new_json = json.dumps(new_rules)

        prompt = f"""Compare these NEW regulatory rules against EXISTING rules and identify any conflicts or contradictions.

EXISTING RULES:
{existing_json}

NEW RULES:
{new_json}

For each conflict found, provide:
- new_rule_id: ID of the new rule
- new_rule_title: Title of the new rule
- existing_rule_id: ID of the conflicting existing rule
- existing_rule_title: Title of the existing rule
- conflict_type: "CONTRADICTS", "SUPERSEDED", or "OVERLAPS"
- severity: "High", "Medium", or "Low"
- reason: Detailed explanation of the conflict

Respond with valid JSON: {{"conflicts": [...]}}
If no conflicts, respond: {{"conflicts": []}}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        response_text = response.text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        result = json.loads(response_text.strip())
        return result.get("conflicts", [])

    except Exception as e:
        print(f"Conflict check error: {e}")
        return []


def apply_conflict_flags(db: Session, rules: list[ExtractedRule], conflicts: list[dict]):
    """Update rule records with conflict information."""
    conflict_map = {}
    for conflict in conflicts:
        rule_id = conflict.get("new_rule_id")
        if rule_id not in conflict_map:
            conflict_map[rule_id] = []
        conflict_map[rule_id].append(conflict)

    for rule in rules:
        if rule.rule_id in conflict_map:
            rule.has_conflict = True
            rule.conflict_details = json.dumps(conflict_map[rule.rule_id])

    db.commit()
