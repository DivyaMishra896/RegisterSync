"""
Suraksha — Application Configuration
Loads settings from .env file with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # LLM Mode: "mock" or "live"
    LLM_MODE: str = os.getenv("LLM_MODE", "mock")

    # Database
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
