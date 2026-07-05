from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Company, JobPosting, JobSkill, Skill
from app.repositories.base_repository import BaseRepository


class JobPostingRepository(BaseRepository[JobPosting]):
    def __init__(self, session: Session) -> None:
        super().__init__(JobPosting, session)

    def get_by_company(self, company_id: int) -> list[JobPosting]:
        result = self.session.execute(select(JobPosting).where(JobPosting.company_id == company_id))
        return list(result.scalars().all())

    def get_detail(self, job_posting_id: int) -> JobPosting | None:
        statement = (
            select(JobPosting)
            .options(
                selectinload(JobPosting.company),
                selectinload(JobPosting.job_skills).selectinload(JobSkill.skill),
            )
            .where(JobPosting.id == job_posting_id)
        )
        result = self.session.execute(statement)
        return result.scalars().first()

    def search(
        self,
        *,
        q: str | None = None,
        job_category: str | None = None,
        company_name: str | None = None,
        location: str | None = None,
        experience_level: str | None = None,
        skill: str | None = None,
        deadline_from=None,
        deadline_to=None,
        is_active: bool | None = True,
        offset: int = 0,
        limit: int = 20,
    ) -> list[JobPosting]:
        statement = (
            select(JobPosting)
            .join(JobPosting.company)
            .options(
                selectinload(JobPosting.company),
                selectinload(JobPosting.job_skills).selectinload(JobSkill.skill),
            )
            .order_by(JobPosting.deadline.is_(None), JobPosting.deadline, JobPosting.id.desc())
        )

        if skill:
            statement = statement.join(JobPosting.job_skills).join(JobSkill.skill)

        if q:
            keyword = f"%{q}%"
            statement = statement.where(
                JobPosting.title.ilike(keyword)
                | JobPosting.description.ilike(keyword)
                | Company.name.ilike(keyword)
            )
        if job_category:
            statement = statement.where(JobPosting.job_category == job_category)
        if company_name:
            statement = statement.where(Company.name.ilike(f"%{company_name}%"))
        if location:
            statement = statement.where(JobPosting.location.ilike(f"%{location}%"))
        if experience_level:
            statement = statement.where(JobPosting.experience_level.ilike(f"%{experience_level}%"))
        if skill:
            statement = statement.where(Skill.name.ilike(f"%{skill}%"))
        if deadline_from:
            statement = statement.where(JobPosting.deadline >= deadline_from)
        if deadline_to:
            statement = statement.where(JobPosting.deadline <= deadline_to)
        if is_active is not None:
            statement = statement.where(JobPosting.is_active.is_(is_active))

        result = self.session.execute(statement.offset(offset).limit(limit))
        return list(result.scalars().unique().all())
