from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Bookmark
from app.repositories.bookmark_repository import BookmarkRepository
from app.repositories.job_posting_repository import JobPostingRepository
from app.repositories.user_repository import UserRepository


class BookmarkService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = BookmarkRepository(db)
        self.job_repository = JobPostingRepository(db)
        self.user_repository = UserRepository(db)

    def add_bookmark(self, user_id: int, job_posting_id: int) -> Bookmark:
        self.user_repository.ensure_user(user_id)
        if not self.job_repository.get_by_id(job_posting_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        bookmark = self.repository.get_by_user_and_job(user_id, job_posting_id)
        if bookmark:
            return bookmark

        bookmark = Bookmark(user_id=user_id, job_posting_id=job_posting_id)
        return self.repository.add(bookmark)

    def delete_bookmark(self, user_id: int, job_posting_id: int) -> None:
        bookmark = self.repository.get_by_user_and_job(user_id, job_posting_id)
        if not bookmark:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
        self.repository.delete(bookmark)
