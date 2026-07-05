from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Bookmark
from app.repositories.base_repository import BaseRepository


class BookmarkRepository(BaseRepository[Bookmark]):
    def __init__(self, session: Session) -> None:
        super().__init__(Bookmark, session)

    def get_by_user_and_job(self, user_id: int, job_posting_id: int) -> Bookmark | None:
        result = self.session.execute(
            select(Bookmark).where(
                Bookmark.user_id == user_id,
                Bookmark.job_posting_id == job_posting_id,
            )
        )
        return result.scalars().first()
