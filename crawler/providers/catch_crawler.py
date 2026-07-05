from __future__ import annotations

from crawler.core.base_crawler import BaseCrawler
from crawler.core.models import JobPostingRawData


class CatchCrawler(BaseCrawler):
    provider_name = "catch"

    def crawl(self, query: str | None = None, limit: int = 20) -> list[JobPostingRawData]:
        """Placeholder for real Catch crawling implementation."""
        return []

    def validate_config(self) -> None:
        return None
