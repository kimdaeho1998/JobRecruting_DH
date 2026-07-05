import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    database_url: Optional[str] = os.getenv("DATABASE_URL")


settings = Settings()
