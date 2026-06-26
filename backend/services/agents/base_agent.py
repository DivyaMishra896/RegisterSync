from services.llm_provider import llm_client

class BaseAgent:
    def __init__(self):
        self.name = "Base Agent"
        self.role = "You are a helpful AI assistant."

    async def think(self, user_prompt: str) -> dict:
        return await llm_client.generate(self.role, user_prompt)
