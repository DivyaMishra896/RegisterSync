import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    LLM_MODE: str = os.getenv("LLM_MODE", "mock")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./suraksha.db")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(Path(__file__).parent / "uploads"))
    MOCK_LOGS_DIR: str = str(Path(__file__).parent / "mock_logs")
    SAMPLES_DIR: str = str(Path(__file__).parent / "samples")

    @classmethod
    def init(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)


settings = Settings()
