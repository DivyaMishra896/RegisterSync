"""
Suraksha — Department Router Service (Hybrid: Keyword-Filter + Round-Robin)

Routing Strategy (Option C — Hybrid):
1. Keyword matching scores all 10 departments for relevance to a rule.
2. Departments with score >= threshold are shortlisted.
3. Round-robin selects the next department from the shortlist.

This ensures assignments are logically correct (keyword filter) AND
fairly distributed (round-robin within the relevant set).
"""

import json
import os
from pathlib import Path
from services.department_data import (
    BUSINESS_VERTICALS,
    DEPARTMENT_NAMES,
    get_default_owner,
    match_sub_vertical,
)

# Minimum keyword score to be considered "relevant" for a rule
RELEVANCE_THRESHOLD = 1

# State file for persisting round-robin counter across restarts
STATE_FILE = Path(__file__).parent.parent / "assignment_state.json"


class CircularAssigner:
    """
    Hybrid Keyword-Filter + Round-Robin assigner.

    For each rule:
    1. Score all 10 departments by keyword matches.
    2. Filter to departments with score >= RELEVANCE_THRESHOLD.
    3. If multiple qualify, pick the next one in round-robin order.
    4. If none qualify, round-robin across ALL departments (fallback).
    """
    _index = 0
    _initialized = False

    @classmethod
    def _load_state(cls):
        """Load persisted index from disk."""
        if cls._initialized:
            return
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                    cls._index = data.get("index", 0)
        except Exception:
            cls._index = 0
        cls._initialized = True

    @classmethod
    def _save_state(cls):
        """Persist index to disk so it survives restarts."""
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"index": cls._index}, f)
        except Exception:
            pass  # Non-critical — index resets on failure

    @classmethod
    def reset(cls):
        """Reset the counter (useful for testing)."""
        cls._index = 0
        cls._save_state()

    @classmethod
    def assign(cls, text: str) -> dict:
        """
        Assign a department using hybrid keyword-filter + round-robin.

        Args:
            text: Combined title + description of the rule/task.

        Returns:
            {
                "department": str,
                "sub_vertical": str or None,
                "regulator": str or None,
                "advisory": str or None,
                "routing_reason": str,
                "keyword_scores": dict,
            }
        """
        cls._load_state()

        # Step 1: Score all departments by keyword match
        scores = score_departments(text)

        # Step 2: Filter to relevant departments
        relevant = [
            dept for dept, score in scores.items()
            if score >= RELEVANCE_THRESHOLD
        ]

        # Step 3: Round-robin within relevant set (or all if none relevant)
        pool = relevant if relevant else DEPARTMENT_NAMES
        # Find the next department in pool using the global index
        dept = cls._pick_from_pool(pool)

        # Step 4: Find best sub-vertical match
        sv = match_sub_vertical(dept, text)

        # Step 5: Build routing reason
        reason = _build_reason(dept, scores, relevant, sv)

        cls._save_state()

        return {
            "department": dept,
            "sub_vertical": sv["name"] if sv else None,
            "regulator": sv["regulator"] if sv else None,
            "advisory": sv["advisory"] if sv else None,
            "routing_reason": reason,
            "keyword_scores": scores,
        }

    @classmethod
    def _pick_from_pool(cls, pool: list) -> str:
        """Pick the next department from the pool using round-robin."""
        # We iterate through the global DEPARTMENT_NAMES order
        # and pick the first one that's in the pool
        start = cls._index
        for i in range(len(DEPARTMENT_NAMES)):
            candidate = DEPARTMENT_NAMES[(start + i) % len(DEPARTMENT_NAMES)]
            if candidate in pool:
                cls._index = (start + i + 1) % len(DEPARTMENT_NAMES)
                cls._save_state()
                return candidate
        # Should never reach here, but fallback
        dept = pool[0]
        cls._index = (cls._index + 1) % len(DEPARTMENT_NAMES)
        cls._save_state()
        return dept


def score_departments(text: str) -> dict:
    """
    Score all 10 departments by keyword match count.
    Returns {department_name: score}.
    """
    text_lower = text.lower()
    scores = {}
    for vertical in BUSINESS_VERTICALS:
        score = sum(1 for kw in vertical["keywords"] if kw in text_lower)
        scores[vertical["name"]] = score
    return scores


def route_to_department(text: str) -> str:
    """
    Legacy-compatible: return the single best department name.
    Uses keyword scoring (highest score wins), no round-robin.
    """
    scores = score_departments(text)
    if max(scores.values()) == 0:
        return "Compliance Department"  # Default fallback
    return max(scores, key=scores.get)


def route_rule_to_departments(title: str, description: str) -> list[str]:
    """
    Legacy-compatible: return list of departments with score >= 1.
    """
    combined = f"{title} {description}"
    scores = score_departments(combined)
    matched = [dept for dept, score in scores.items() if score >= 1]
    return matched if matched else ["Compliance Department"]


def get_department_color(department: str) -> str:
    """Get the display color for a department."""
    from services.department_data import DEPARTMENT_COLORS
    return DEPARTMENT_COLORS.get(department, "#6b7280")


def _build_reason(dept: str, scores: dict, relevant: list, sv: dict | None) -> str:
    """Build a human-readable routing reason."""
    score = scores.get(dept, 0)
    parts = []

    if score > 0:
        parts.append(f"Keyword match score: {score}")
    else:
        parts.append("No direct keyword match — assigned via round-robin rotation")

    if len(relevant) > 1:
        others = [r for r in relevant if r != dept]
        parts.append(f"Also relevant to: {', '.join(others[:3])}")

    if sv:
        parts.append(f"Sub-vertical: {sv['name']} ({sv['scope']})")
        parts.append(f"Applicable advisory: {sv['advisory']}")

    return ". ".join(parts)
