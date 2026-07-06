import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency for local env
    load_dotenv = None


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATABASE_URL = f"sqlite:///{(REPO_ROOT / 'jobinsight_test.db').as_posix()}"
DEFAULT_AI_LOG_PATH = REPO_ROOT / "backend" / "logs" / "ai_calls.jsonl"

if load_dotenv is not None:
    load_dotenv(REPO_ROOT / ".env", override=False)


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    api_v1_prefix: str = "/api/v1"
    ai_mode: str = os.getenv("AI_MODE", "mock")
    ai_mock_mode: Optional[str] = os.getenv("AI_MOCK_MODE")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_timeout: float = float(os.getenv("OPENAI_TIMEOUT", "20"))
    openai_max_retries: int = int(os.getenv("OPENAI_MAX_RETRIES", "2"))
    ai_log_path: str = os.getenv("AI_LOG_PATH", str(DEFAULT_AI_LOG_PATH))


settings = Settings()
