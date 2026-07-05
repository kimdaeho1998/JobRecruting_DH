from __future__ import annotations

from crawler.core.base_crawler import BaseCrawler
from crawler.core.models import JobPostingRawData


class WantedCrawler(BaseCrawler):
    provider_name = "wanted"

    def crawl(self, query: str | None = None, limit: int = 20) -> list[JobPostingRawData]:
        """Placeholder for real Wanted crawling implementation."""
        return []

    def validate_config(self) -> None:
        return None
