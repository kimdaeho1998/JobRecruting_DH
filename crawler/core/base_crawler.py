from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from crawler.core.models import JobPostingRawData


class BaseCrawler(ABC):
    """Base interface for site-specific crawlers."""

    provider_name: str

    @abstractmethod
    def crawl(self, query: str | None = None, limit: int = 20) -> list[JobPostingRawData]:
        """Collect postings from a provider and return a shared raw format."""

    @abstractmethod
    def validate_config(self) -> None:
        """Validate provider-specific configuration before crawl."""

    def build_context(self, **kwargs: Any) -> dict[str, Any]:
        return {"provider": self.provider_name, **kwargs}
