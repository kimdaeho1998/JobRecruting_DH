from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company
from app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session: Session) -> None:
        super().__init__(Company, session)

    def get_by_name(self, name: str) -> Company | None:
        result = self.session.execute(select(Company).where(Company.name == name))
        return result.scalars().first()

    def search_by_name(self, name: str | None = None) -> list[Company]:
        statement = select(Company).order_by(Company.name)
        if name:
            statement = statement.where(Company.name.ilike(f"%{name}%"))
        result = self.session.execute(statement)
        return list(result.scalars().all())
