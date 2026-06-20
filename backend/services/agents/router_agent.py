"""
Suraksha — Router Agent
Assigns rules to departments with reasoning.
Uses 10 Business Verticals from Theme 2.
"""

import json
from services.agents.base_agent import BaseAgent
from services.department_router import route_rule_to_departments
from services.department_data import DEPARTMENT_NAMES

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "Router Agent"
        dept_list = ", ".join(DEPARTMENT_NAMES)
        self.role = (
            "You are a compliance task router for an Indian bank. Given a regulatory rule title and description, "
            "determine which departments should handle it and explain why. "
            f"Available departments: {dept_list}. "
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
