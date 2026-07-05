from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.company_repository import CompanyRepository
from app.repositories.skill_repository import SkillRepository


class CatalogService:
    def __init__(self, db: Session) -> None:
        self.company_repository = CompanyRepository(db)
        self.skill_repository = SkillRepository(db)

    def list_companies(self, name: str | None = None):
        return self.company_repository.search_by_name(name)

    def list_skills(self, name: str | None = None):
        return self.skill_repository.search_by_name(name)
