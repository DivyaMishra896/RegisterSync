import json
import os
from pathlib import Path
from services.department_data import (
    BUSINESS_VERTICALS,
    DEPARTMENT_NAMES,
    get_default_owner,
    match_sub_vertical,
)

# Threshold
RELEVANCE_THRESHOLD = 1

# State file
STATE_FILE = Path(__file__).parent.parent / "assignment_state.json"


class CircularAssigner:
    _index = 0
    _initialized = False

    @classmethod
    def _load_state(cls):
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
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"index": cls._index}, f)
        except Exception:
            pass

    @classmethod
    def reset(cls):
        cls._index = 0
        cls._save_state()

    @classmethod
    def assign(cls, text: str) -> dict:
        cls._load_state()

        scores = score_departments(text)

        relevant = [
            dept for dept, score in scores.items()
            if score >= RELEVANCE_THRESHOLD
        ]

        pool = relevant if relevant else DEPARTMENT_NAMES
        dept = cls._pick_from_pool(pool)

        sv = match_sub_vertical(dept, text)

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
        start = cls._index
        for i in range(len(DEPARTMENT_NAMES)):
            candidate = DEPARTMENT_NAMES[(start + i) % len(DEPARTMENT_NAMES)]
            if candidate in pool:
                cls._index = (start + i + 1) % len(DEPARTMENT_NAMES)
                cls._save_state()
                return candidate
        dept = pool[0]
        cls._index = (cls._index + 1) % len(DEPARTMENT_NAMES)
        cls._save_state()
        return dept


def score_departments(text: str) -> dict:
    text_lower = text.lower()
    scores = {}
    for vertical in BUSINESS_VERTICALS:
        score = sum(1 for kw in vertical["keywords"] if kw in text_lower)
        scores[vertical["name"]] = score
    return scores


def route_to_department(text: str) -> str:
    scores = score_departments(text)
    if max(scores.values()) == 0:
        return "Compliance Department"
    return max(scores, key=scores.get)


def route_rule_to_departments(title: str, description: str) -> list[str]:
    combined = f"{title} {description}"
    scores = score_departments(combined)
    matched = [dept for dept, score in scores.items() if score >= 1]
    return matched if matched else ["Compliance Department"]


def get_department_color(department: str) -> str:
    from services.department_data import DEPARTMENT_COLORS
    return DEPARTMENT_COLORS.get(department, "#6b7280")


def _build_reason(dept: str, scores: dict, relevant: list, sv: dict | None) -> str:
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
