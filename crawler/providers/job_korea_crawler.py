from __future__ import annotations

from crawler.core.base_crawler import BaseCrawler
from crawler.core.models import JobPostingRawData


class JobKoreaCrawler(BaseCrawler):
    provider_name = "jobkorea"

    def crawl(self, query: str | None = None, limit: int = 20) -> list[JobPostingRawData]:
        """Placeholder for real JobKorea crawling implementation."""
        return []

    def validate_config(self) -> None:
        return None
