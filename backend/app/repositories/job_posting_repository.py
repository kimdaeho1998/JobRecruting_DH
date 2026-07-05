from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import JobPosting
from app.repositories.base_repository import BaseRepository


class JobPostingRepository(BaseRepository[JobPosting]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(JobPosting, session)

    async def get_by_company(self, company_id: int) -> list[JobPosting]:
        result = await self.session.execute(select(JobPosting).where(JobPosting.company_id == company_id))
        return list(result.scalars().all())
