import os
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATABASE_URL = f"sqlite:///{(REPO_ROOT / 'jobinsight_test.db').as_posix()}"


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    api_v1_prefix: str = "/api/v1"


settings = Settings()
