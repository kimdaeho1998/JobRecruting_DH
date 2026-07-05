from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Optional


@dataclass
class JobPostingRawData:
    """Normalized raw structure returned by any provider."""

    provider: str
    source_site: str
    source_id: str
    title: str
    company_name: str
    company_id: Optional[str] = None
    job_category: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    description: Optional[str] = None
    salary_range: Optional[str] = None
    deadline: Optional[date] = None
    source_url: Optional[str] = None
    is_active: bool = True
    skills: list[str] = field(default_factory=list)
    raw_payload: dict[str, Any] = field(default_factory=dict)
    collected_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CrawlLogEntry:
    """Represents a single crawl execution log entry."""

    provider: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str = "pending"
    items_found: int = 0
    items_new: int = 0
    items_duplicates: int = 0
    error: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
