from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Skill
from app.repositories.base_repository import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, session: Session) -> None:
        super().__init__(Skill, session)

    def search_by_name(self, name: str | None = None) -> list[Skill]:
        statement = select(Skill).order_by(Skill.name)
        if name:
            statement = statement.where(Skill.name.ilike(f"%{name}%"))
        result = self.session.execute(statement)
        return list(result.scalars().all())
