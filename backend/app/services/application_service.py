from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Application
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_posting_repository import JobPostingRepository
from app.repositories.user_repository import UserRepository
from app.schemas import ApplicationUpdate


class ApplicationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = ApplicationRepository(db)
        self.job_repository = JobPostingRepository(db)
        self.user_repository = UserRepository(db)

    def list_applications(self, user_id: int = 1) -> list[dict]:
        self.user_repository.ensure_user(user_id)
        applications = self.repository.list_by_user(user_id)
        return [self._to_list_item(application) for application in applications]

    def create_application(
        self,
        *,
        user_id: int,
        job_posting_id: int,
        status_value: str,
        notes: str | None = None,
    ) -> Application:
        self.user_repository.ensure_user(user_id)
        if not self.job_repository.get_by_id(job_posting_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        application = self.repository.get_by_user_and_job(user_id, job_posting_id)
        if application:
            application.status = status_value
            application.notes = notes
        else:
            application = Application(
                user_id=user_id,
                job_posting_id=job_posting_id,
                status=status_value,
                notes=notes,
            )
            self.db.add(application)

        if status_value == "applied" and application.applied_at is None:
            application.applied_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(application)
        return application

    def update_application(self, application_id: int, payload: ApplicationUpdate) -> Application:
        application = self.repository.get_by_id(application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

        if payload.status is not None:
            application.status = payload.status
            if payload.status == "applied" and application.applied_at is None:
                application.applied_at = datetime.utcnow()
        if payload.notes is not None:
            application.notes = payload.notes
        if payload.applied_at is not None:
            application.applied_at = payload.applied_at

        self.db.commit()
        self.db.refresh(application)
        return application

    def _to_list_item(self, application: Application) -> dict:
        job_posting = application.job_posting
        return {
            "id": application.id,
            "user_id": application.user_id,
            "job_posting_id": application.job_posting_id,
            "status": application.status,
            "notes": application.notes,
            "applied_at": application.applied_at,
            "created_at": application.created_at,
            "updated_at": application.updated_at,
            "job_title": job_posting.title if job_posting else None,
            "company_name": job_posting.company.name if job_posting and job_posting.company else None,
        }
