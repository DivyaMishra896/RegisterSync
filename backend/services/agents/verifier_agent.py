"""
Suraksha — Verifier Agent
Checks system logs to verify task completion using LLM reasoning.
"""

from services.agents.base_agent import BaseAgent

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "Verifier Agent"
        self.role = (
            "You are a compliance verification agent. Given a compliance task description and a system log entry, "
            "determine if the log entry proves the task was completed. "
            "Classify as: Verified (clear evidence), Partially Done (some evidence), Failed (contradictory evidence), or No Evidence. "
            "Explain your reasoning. "
            "Respond ONLY with a valid JSON object matching this schema: "
            "{'status': string, 'reasoning': string}"
        )

    async def verify(self, task_description: str, log_entry: dict) -> dict:
        prompt = (
            f"TASK: {task_description}\n\n"
            f"LOG ENTRY:\n{log_entry}\n\n"
            "Verify the task."
        )
        result = await self.think(prompt)
        
        if not result or "status" not in result:
            # Fallback handled in the calling service
            return {"status": "Unknown", "reasoning": "Fallback to manual verification."}
            
        return result
