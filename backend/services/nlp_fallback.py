import re
import json
from datetime import date, timedelta
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    pass

REGULATORY_KEYWORDS = [
    "rbi", "sebi", "irdai", "nabard", "circular", "directive", "regulation",
    "compliance", "shall", "must", "mandatory", "prescribed", "guidelines",
    "banks", "banking", "financial institution", "regulated entity",
    "master direction", "notification", "gazette", "prudential", "statutory",
    "penalty", "enforcement", "deadline", "submit", "report to", "supervisory",
    "capital adequacy", "kyc", "aml", "fraud", "npa", "nbfc", "payment system",
]
_MIN_KEYWORD_HITS = 3


def is_regulatory_document(text: str) -> bool:
    lower = text.lower()
    hits = sum(1 for kw in REGULATORY_KEYWORDS if kw in lower)
    return hits >= _MIN_KEYWORD_HITS


def mock_read_circular(text: str) -> dict:
    if not is_regulatory_document(text):
        return {
            "subject": "Non-Regulatory Document",
            "reference": "",
            "summary": "This document does not appear to be a regulatory circular.",
            "regulatory_sections": [],
            "info_sections": [],
            "is_regulatory": False,
        }

    paragraphs = text.split('\n\n')
    summary = "Mock summary of regulatory text."
    if paragraphs:
        summary = paragraphs[0][:200] + "..."

    return {
        "subject": "Mock RBI Circular",
        "reference": "RBI/2026/01",
        "summary": summary,
        "regulatory_sections": paragraphs[:5],
        "info_sections": paragraphs[5:],
        "is_regulatory": True,
    }

def mock_extract_rules(sections: list) -> list:
    if not sections:
        return []

    rules = []
    for i, section in enumerate(sections):
        if i >= 4:
            break
            
        words = section.split()
        if len(words) < 5:
            continue
            
        title = " ".join(words[:10]).title() + "..."
        
        rules.append({
            "rule_id": f"R-MOCK-{len(section)}{i}",
            "title": title,
            "description": section[:250].strip() + ("..." if len(section) > 250 else ""),
            "affected_departments": ["Compliance Department", "Risk Management"],
            "deadline": (date.today() + timedelta(days=60)).isoformat(),
            "priority": "High" if i % 2 == 0 else "Medium",
            "estimated_effort_days": 15 + (i * 5)
        })
        
    return rules

def mock_check_conflicts(new_rules: list, existing_rules: list) -> list:
    try:
        if not new_rules or not existing_rules:
            return []

        vectorizer = TfidfVectorizer(stop_words='english')
        
        new_texts = [r.get("title", "") + " " + r.get("description", "") for r in new_rules]
        existing_texts = [r.get("title", "") + " " + r.get("description", "") for r in existing_rules]
        
        all_texts = new_texts + existing_texts
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        new_matrix = tfidf_matrix[:len(new_rules)]
        existing_matrix = tfidf_matrix[len(new_rules):]
        
        similarity = cosine_similarity(new_matrix, existing_matrix)
        
        conflicts = []
        for i, new_rule in enumerate(new_rules):
            for j, existing_rule in enumerate(existing_rules):
                if similarity[i][j] > 0.4:
                    conflicts.append({
                        "new_rule_id": new_rule.get("rule_id", "Unknown"),
                        "new_rule_title": new_rule.get("title", "Unknown"),
                        "existing_rule_id": existing_rule.get("rule_id", "Unknown"),
                        "existing_rule_title": existing_rule.get("title", "Unknown"),
                        "conflict_type": "OVERLAPS",
                        "severity": "Medium",
                        "reason": f"Semantic overlap detected (Similarity score: {similarity[i][j]:.2f}). Needs manual review to confirm if requirements contradict."
                    })
        return conflicts
    except Exception as e:
        print(f"[NLP Fallback] Conflict check error: {e}")
        return []
