import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str | None = os.getenv("DATABASE_URL")


settings = Settings()
