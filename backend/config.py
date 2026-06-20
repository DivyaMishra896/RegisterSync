"""
Suraksha — Application Configuration
Loads settings from .env file with sensible defaults.
Supports Ollama (local LLM) with swappable models.
Fully offline — no external API keys needed.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # LLM Mode: "ollama" (local AI) or "mock" (regex fallback, no AI needed)
    LLM_MODE: str = os.getenv("LLM_MODE", "mock")

    # Ollama Configuration — swap models by changing OLLAMA_MODEL
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")

    # Database (SQLite for offline use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./suraksha.db")

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # File storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(Path(__file__).parent / "uploads"))
    MOCK_LOGS_DIR: str = str(Path(__file__).parent / "mock_logs")
    SAMPLES_DIR: str = str(Path(__file__).parent / "samples")

    # Ensure upload directory exists
    @classmethod
    def init(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)


settings = Settings()
