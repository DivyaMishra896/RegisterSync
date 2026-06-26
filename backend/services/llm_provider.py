import json
import httpx
from config import settings

class LLMProvider:
    def __init__(self):
        self.mode = settings.LLM_MODE
        self.ollama_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL

    async def generate(self, system_prompt: str, user_prompt: str) -> dict:
        if self.mode == "mock":
            return {}

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json"
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(f"{self.ollama_url}/api/chat", json=payload)
                response.raise_for_status()
                data = response.json()
                content = data.get("message", {}).get("content", "{}")
                
                return self._parse_json(content)
        except Exception as e:
            print(f"[LLMProvider] Error calling Ollama: {e}")
            return {}

    def _parse_json(self, text: str) -> dict:
        try:
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            print(f"[LLMProvider] Failed to parse JSON from: {text}")
            return {}

llm_client = LLMProvider()
