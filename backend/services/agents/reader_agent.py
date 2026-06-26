from services.agents.base_agent import BaseAgent
from services.nlp_fallback import mock_read_circular

class ReaderAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "Reader Agent"
        self.role = (
            "You are a regulatory document analyst for Indian banking. "
            "Given raw text from an RBI/SEBI circular, identify: "
            "(1) the circular's subject and reference number, "
            "(2) which sections contain mandatory regulatory requirements vs informational context, "
            "(3) a brief summary. "
            "Respond ONLY with a valid JSON object matching this schema: "
            "{'subject': string, 'reference': string, 'summary': string, 'regulatory_sections': list[string], 'info_sections': list[string]}"
        )

    async def analyze(self, text: str) -> dict:
        result = await self.think(f"Analyze this regulatory text:\n\n{text}")
        if not result:
            return mock_read_circular(text)
        return result
