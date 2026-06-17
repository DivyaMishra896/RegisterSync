"""
Suraksha — Router Agent
Assigns rules to departments with reasoning.
"""

import json
from services.agents.base_agent import BaseAgent
from services.department_router import route_rule_to_departments

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "Router Agent"
        self.role = (
            "You are a compliance task router for an Indian bank. Given a regulatory rule title and description, "
            "determine which departments should handle it and explain why. "
            "Available departments: IT Security, Risk Management, Operations. "
            "Respond ONLY with a valid JSON object matching this schema: "
            "{'departments': [list of strings], 'reasoning': string}"
        )

    async def assign(self, title: str, description: str) -> dict:
        prompt = f"TITLE: {title}\nDESCRIPTION: {description}\n\nAssign departments."
        result = await self.think(prompt)
        
        if not result or "departments" not in result:
            # Fallback
            depts = route_rule_to_departments(title, description)
            return {"departments": depts, "reasoning": "Assigned using fallback keyword matching."}
            
        return result
