from __future__ import annotations

from typing import Any

from crawler.core.base_crawler import BaseCrawler
from crawler.core.models import CrawlLogEntry, JobPostingRawData
from crawler.core.normalizer import Normalizer
from crawler.core.deduplication_service import DeduplicationService


class CrawlRunner:
    """Coordinate providers, normalization, deduplication, and logging."""

    def __init__(self, crawlers: list[BaseCrawler] | None = None) -> None:
        self.crawlers = crawlers or []
        self.normalizer = Normalizer()
        self.dedup = DeduplicationService()

    def run(self, query: str | None = None, limit: int = 20) -> tuple[list[JobPostingRawData], list[CrawlLogEntry]]:
        logs: list[CrawlLogEntry] = []
        collected: list[JobPostingRawData] = []

        for crawler in self.crawlers:
            crawler.validate_config()
            log = CrawlLogEntry(provider=crawler.provider_name, started_at=__import__("datetime").datetime.utcnow())
            try:
                raw_items = crawler.crawl(query=query, limit=limit)
                normalized = [self.normalizer.normalize(crawler.provider_name, item) for item in raw_items]
                unique = self.dedup.filter_duplicates(normalized)
                collected.extend(unique)
                log.status = "success"
                log.items_found = len(normalized)
                log.items_new = len(unique)
                log.items_duplicates = len(normalized) - len(unique)
            except Exception as exc:  # pragma: no cover - structure placeholder
                log.status = "failed"
                log.error = str(exc)
            finally:
                log.finished_at = __import__("datetime").datetime.utcnow()
                logs.append(log)

        return collected, logs
