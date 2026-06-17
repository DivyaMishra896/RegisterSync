"""
Suraksha — Extractor Agent
Extracts structured rules from regulatory sections.
"""

import json
from services.agents.base_agent import BaseAgent
from services.nlp_fallback import mock_extract_rules

class ExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "Extractor Agent"
        self.role = (
            "You are a compliance rules extractor. Given regulatory text sections from an Indian banking circular, "
            "extract each distinct regulatory requirement as a structured rule. "
            "For each rule provide: "
            "- rule_id: string (e.g., R-001) "
            "- title: string "
            "- description: string "
            "- affected_departments: list of strings (from: IT Security, Risk Management, Operations) "
            "- deadline: string (ISO format YYYY-MM-DD or null) "
            "- priority: string (Critical, High, Medium, Low) "
            "- estimated_effort_days: integer "
            "Respond ONLY with a valid JSON object matching this schema: {'rules': [rule_objects]}"
        )

    async def extract(self, sections: list) -> list:
        combined_text = "\n\n".join(sections)
        result = await self.think(f"Extract rules from these sections:\n\n{combined_text}")
        if not result or "rules" not in result:
            return mock_extract_rules(sections)
        return result.get("rules", [])
