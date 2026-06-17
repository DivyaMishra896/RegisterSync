"""
Suraksha — Conflict Agent
Compares new rules against existing rules and finds contradictions.
"""

import json
from services.agents.base_agent import BaseAgent
from services.nlp_fallback import mock_check_conflicts

class ConflictAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "Conflict Agent"
        self.role = (
            "You are a regulatory conflict analyst. Compare NEW rules against EXISTING rules and identify conflicts. "
            "For each conflict: classify as CONTRADICTS, SUPERSEDED, or OVERLAPS, assign severity (High, Medium, Low), "
            "and explain your reasoning. "
            "Respond ONLY with a valid JSON object matching this schema: "
            "{'conflicts': [{'new_rule_id': string, 'new_rule_title': string, 'existing_rule_id': string, 'existing_rule_title': string, 'conflict_type': string, 'severity': string, 'reason': string}]}"
        )

    async def find_conflicts(self, new_rules: list, existing_rules: list) -> list:
        if not existing_rules:
            return []
            
        prompt = (
            f"EXISTING RULES:\n{json.dumps(existing_rules)}\n\n"
            f"NEW RULES:\n{json.dumps(new_rules)}\n\n"
            "Identify any conflicts."
        )
        result = await self.think(prompt)
        
        if not result or "conflicts" not in result:
            return mock_check_conflicts(new_rules, existing_rules)
            
        return result.get("conflicts", [])
