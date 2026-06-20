"""
Suraksha — Conflict Checker Service
Detects conflicts between new rules and existing rules in the database.
Uses semantic comparison to flag contradictions.
Fully offline — uses TF-IDF or mock data.
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

    # Ollama mode: compare against existing rules in DB
    existing_rules = db.query(ExtractedRule).all()

    if not existing_rules:
        return []

    # Use TF-IDF for semantic comparison (offline)
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        existing_data = [{
            "rule_id": r.rule_id,
            "title": r.title,
            "description": r.description
        } for r in existing_rules]

        new_texts = [r.get("title", "") + " " + r.get("description", "") for r in new_rules]
        existing_texts = [r["title"] + " " + r["description"] for r in existing_data]

        all_texts = new_texts + existing_texts
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        new_matrix = tfidf_matrix[:len(new_rules)]
        existing_matrix = tfidf_matrix[len(new_rules):]
        similarity = cosine_similarity(new_matrix, existing_matrix)

        conflicts = []
        for i, new_rule in enumerate(new_rules):
            for j, existing_rule in enumerate(existing_data):
                if similarity[i][j] > 0.4:
                    conflicts.append({
                        "new_rule_id": new_rule.get("rule_id", "Unknown"),
                        "new_rule_title": new_rule.get("title", "Unknown"),
                        "existing_rule_id": existing_rule["rule_id"],
                        "existing_rule_title": existing_rule["title"],
                        "conflict_type": "OVERLAPS",
                        "severity": "Medium",
                        "reason": f"Semantic overlap detected (Similarity: {similarity[i][j]:.2f}). Needs manual review."
                    })
        return conflicts
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
