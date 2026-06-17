"""
Suraksha — LLM Provider
Unified interface for LLM interactions. Supports local Ollama and a mock fallback.
"""

import json
import httpx
from config import settings

class LLMProvider:
    def __init__(self):
        self.mode = settings.LLM_MODE
        self.ollama_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL

    async def generate(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Generate a response from the LLM. 
        Returns parsed JSON if the LLM output is valid JSON, otherwise tries to extract JSON.
        """
        if self.mode == "mock":
            # In mock mode, the caller usually provides its own fallback logic.
            # We return empty to let the agent use its nlp_fallback.
            return {}

        # Ollama API payload
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json" # Force JSON output if the model supports it
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
            # Fallback on failure
            return {}

    def _parse_json(self, text: str) -> dict:
        """Helper to safely parse JSON from LLM output."""
        try:
            # Handle markdown blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            print(f"[LLMProvider] Failed to parse JSON from: {text}")
            return {}

# Singleton instance
llm_client = LLMProvider()
