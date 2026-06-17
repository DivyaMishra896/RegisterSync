"""
Suraksha — NLP Fallback Methods
Provides regex, keyword matching, and TF-IDF logic when LLM_MODE="mock".
"""

import re
import json
from datetime import date, timedelta
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    pass # Handled gracefully if not installed

def mock_read_circular(text: str) -> dict:
    """Mock reader agent using regex."""
    paragraphs = text.split('\n\n')
    summary = "Mock summary of regulatory text."
    if paragraphs:
        summary = paragraphs[0][:200] + "..."

    return {
        "subject": "Mock RBI Circular",
        "reference": "RBI/2026/01",
        "summary": summary,
        "regulatory_sections": paragraphs[:5],
        "info_sections": paragraphs[5:]
    }

def mock_extract_rules(sections: list) -> list:
    """Mock extractor agent."""
    rules = []
    rule_id_counter = 1
    
    # We use a hardcoded fallback for consistent demo if no AI is available
    return [
        {
            "rule_id": "R-001",
            "title": "Mandatory VAPT Assessment for Core Banking Systems",
            "description": "All scheduled commercial banks shall conduct Vulnerability Assessment and Penetration Testing (VAPT) of their core banking systems, internet banking platforms, and mobile banking applications at least once every six months.",
            "affected_departments": ["IT Security"],
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 21
        },
        {
            "rule_id": "R-002",
            "title": "Enhanced Customer Due Diligence for High-Risk Accounts",
            "description": "Banks shall implement enhanced due diligence procedures for accounts classified as high-risk under the risk-based approach. This includes periodic review of KYC documents every 6 months.",
            "affected_departments": ["Operations", "Risk Management"],
            "deadline": (date.today() + timedelta(days=60)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 30
        }
    ]

def mock_check_conflicts(new_rules: list, existing_rules: list) -> list:
    """Mock conflict agent using TF-IDF."""
    try:
        if not new_rules or not existing_rules:
            return []

        # Simple TF-IDF cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        
        new_texts = [r.get("title", "") + " " + r.get("description", "") for r in new_rules]
        existing_texts = [r.get("title", "") + " " + r.get("description", "") for r in existing_rules]
        
        all_texts = new_texts + existing_texts
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate similarity between new and existing
        new_matrix = tfidf_matrix[:len(new_rules)]
        existing_matrix = tfidf_matrix[len(new_rules):]
        
        similarity = cosine_similarity(new_matrix, existing_matrix)
        
        conflicts = []
        for i, new_rule in enumerate(new_rules):
            for j, existing_rule in enumerate(existing_rules):
                if similarity[i][j] > 0.4: # Threshold
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
