from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.models import JobPosting
from app.repositories.job_posting_repository import JobPostingRepository


class JobPostingService:
    def __init__(self, db: Session) -> None:
        self.repository = JobPostingRepository(db)

    def list_job_postings(
        self,
        *,
        q: str | None = None,
        job_category: str | None = None,
        company_name: str | None = None,
        location: str | None = None,
        experience_level: str | None = None,
        skill: str | None = None,
        deadline_from: date | None = None,
        deadline_to: date | None = None,
        is_active: bool | None = True,
        offset: int = 0,
        limit: int = 20,
    ) -> list[dict]:
        postings = self.repository.search(
            q=q,
            job_category=job_category,
            company_name=company_name,
            location=location,
            experience_level=experience_level,
            skill=skill,
            deadline_from=deadline_from,
            deadline_to=deadline_to,
            is_active=is_active,
            offset=offset,
            limit=limit,
        )
        return [self._to_summary(posting) for posting in postings]

    def get_job_posting(self, job_posting_id: int) -> dict | None:
        posting = self.repository.get_detail(job_posting_id)
        if not posting:
            return None
        return self._to_detail(posting)

    def _to_summary(self, posting: JobPosting) -> dict:
        return {
            "id": posting.id,
            "company_id": posting.company_id,
            "company_name": posting.company.name if posting.company else "",
            "title": posting.title,
            "job_category": posting.job_category,
            "location": posting.location,
            "job_type": posting.job_type,
            "experience_level": posting.experience_level,
            "salary_range": posting.salary_range,
            "deadline": posting.deadline,
            "source_site": posting.source_site,
            "source_url": posting.source_url,
            "is_active": posting.is_active,
            "skills": [job_skill.skill.name for job_skill in posting.job_skills if job_skill.skill],
        }

    def _to_detail(self, posting: JobPosting) -> dict:
        data = self._to_summary(posting)
        data.update(
            {
                "description": posting.description,
                "created_at": posting.created_at,
                "updated_at": posting.updated_at,
            }
        )
        return data
