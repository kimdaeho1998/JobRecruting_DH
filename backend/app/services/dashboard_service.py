from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Application, Bookmark, Company, CompanyFollow, JobPosting, JobSkill, Skill


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
            "new_job_postings": self._count(JobPosting, JobPosting.created_at >= datetime.now(timezone.utc) - timedelta(days=7)),
            "deadline_soon_job_postings": self._count(JobPosting, JobPosting.deadline <= (date.today() + timedelta(days=7)), JobPosting.deadline.is_not(None)),
            "total_companies": self._count(Company),
            "total_skills": self._count(Skill),
            "total_bookmarks": self._count(Bookmark),
            "total_applications": self._count(Application),
            "total_company_follows": self._count(CompanyFollow),
            "applications_by_status": applications_by_status,
            "completed_applications": int(applications_by_status.get("지원 완료", 0) + applications_by_status.get("서류 합격", 0) + applications_by_status.get("최종 합격", 0)),
            "top_skills": self._top_skills(),
            "job_count_by_location": self._counts_by_field(JobPosting.location),
            "job_count_by_category": self._counts_by_field(JobPosting.job_category),
            "application_status_ratio": self._application_status_ratio(applications_by_status),
        }

    def _count(self, model, *conditions) -> int:
        statement = select(func.count(model.id))
        for condition in conditions:
            statement = statement.where(condition)
        return int(self.db.execute(statement).scalar_one())

    def _top_skills(self) -> list[dict[str, object]]:
        rows = self.db.execute(
            select(Skill.name, func.count(JobPosting.id))
            .join(Skill.job_skills)
            .join(JobSkill.job_posting)
            .group_by(Skill.id, Skill.name)
            .order_by(func.count(JobPosting.id).desc())
            .limit(10)
        ).all()
        return [{"name": name, "value": int(count)} for name, count in rows]

    def _counts_by_field(self, field) -> list[dict[str, object]]:
        rows = self.db.execute(
            select(field, func.count(JobPosting.id)).group_by(field).order_by(func.count(JobPosting.id).desc())
        ).all()
        return [{"name": value or "미정", "value": int(count)} for value, count in rows]

    def _application_status_ratio(self, applications_by_status: dict[str, int]) -> list[dict[str, object]]:
        total = sum(applications_by_status.values()) or 1
        return [
            {"name": status, "value": round((count / total) * 100, 1)} for status, count in sorted(applications_by_status.items())
        ]
