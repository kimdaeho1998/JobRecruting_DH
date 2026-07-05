from __future__ import annotations

from typing import Any

from crawler.core.models import JobPostingRawData


class Normalizer:
    """Normalize provider-specific raw payload into a consistent schema."""

    def normalize(self, provider: str, payload: dict[str, Any]) -> JobPostingRawData:
        return JobPostingRawData(
            provider=provider,
            source_site=payload.get("source_site") or provider,
            source_id=str(payload.get("source_id") or payload.get("id") or ""),
            title=str(payload.get("title") or ""),
            company_name=str(payload.get("company_name") or ""),
            company_id=str(payload.get("company_id") or payload.get("company", "")) if payload.get("company_id") or payload.get("company") else None,
            job_category=payload.get("job_category"),
            location=payload.get("location"),
            job_type=payload.get("job_type"),
            experience_level=payload.get("experience_level"),
            description=payload.get("description"),
            salary_range=payload.get("salary_range"),
            deadline=payload.get("deadline"),
            source_url=payload.get("source_url"),
            is_active=bool(payload.get("is_active", True)),
            skills=list(payload.get("skills") or []),
            raw_payload=payload,
        )
