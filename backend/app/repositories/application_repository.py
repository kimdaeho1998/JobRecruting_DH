from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Application, JobPosting
from app.repositories.base_repository import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    def __init__(self, session: Session) -> None:
        super().__init__(Application, session)

    def get_by_user_and_job(self, user_id: int, job_posting_id: int) -> Application | None:
        result = self.session.execute(
            select(Application).where(
                Application.user_id == user_id,
                Application.job_posting_id == job_posting_id,
            )
        )
        return result.scalars().first()

    def list_by_user(self, user_id: int) -> list[Application]:
        result = self.session.execute(
            select(Application)
            .options(selectinload(Application.job_posting).selectinload(JobPosting.company))
            .where(Application.user_id == user_id)
            .order_by(Application.updated_at.desc())
        )
        return list(result.scalars().all())
