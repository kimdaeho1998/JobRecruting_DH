from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CompanyFollow
from app.repositories.base_repository import BaseRepository


class CompanyFollowRepository(BaseRepository[CompanyFollow]):
    def __init__(self, session: Session) -> None:
        super().__init__(CompanyFollow, session)

    def get_by_user_and_company(self, user_id: int, company_id: int) -> CompanyFollow | None:
        result = self.session.execute(
            select(CompanyFollow).where(
                CompanyFollow.user_id == user_id,
                CompanyFollow.company_id == company_id,
            )
        )
        return result.scalars().first()
