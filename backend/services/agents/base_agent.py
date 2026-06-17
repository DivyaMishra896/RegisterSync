"""
Suraksha — Base Agent
Provides common functionality for all specialist agents.
"""

from services.llm_provider import llm_client

class BaseAgent:
    def __init__(self):
        self.name = "Base Agent"
        self.role = "You are a helpful AI assistant."

    async def think(self, user_prompt: str) -> dict:
        """
        Sends the prompt to the LLM and returns the parsed JSON response.
        If in mock mode, this will return {} and the agent's subclass should handle the fallback.
        """
        return await llm_client.generate(self.role, user_prompt)
