from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Application, Bookmark, Company, CompanyFollow, JobPosting, Skill


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_stats(self) -> dict:
        applications_by_status = dict(
            self.db.execute(
                select(Application.status, func.count(Application.id)).group_by(Application.status)
            ).all()
        )

        return {
            "total_job_postings": self._count(JobPosting),
            "active_job_postings": self._count(JobPosting, JobPosting.is_active.is_(True)),
            "total_companies": self._count(Company),
            "total_skills": self._count(Skill),
            "total_bookmarks": self._count(Bookmark),
            "total_applications": self._count(Application),
            "total_company_follows": self._count(CompanyFollow),
            "applications_by_status": applications_by_status,
        }

    def _count(self, model, *conditions) -> int:
        statement = select(func.count(model.id))
        for condition in conditions:
            statement = statement.where(condition)
        return int(self.db.execute(statement).scalar_one())
