from __future__ import annotations

from crawler.core.base_crawler import BaseCrawler
from crawler.core.models import JobPostingRawData


class CompanyCrawler(BaseCrawler):
    provider_name = "company"

    def crawl(self, query: str | None = None, limit: int = 20) -> list[JobPostingRawData]:
        """Placeholder for company-specific enrichment or sourcing."""
        return []

    def validate_config(self) -> None:
        return None
