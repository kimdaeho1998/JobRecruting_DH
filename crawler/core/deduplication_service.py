from __future__ import annotations

from crawler.core.models import JobPostingRawData


class DeduplicationService:
    """Remove duplicate postings based on provider/source identity and title/company combination."""

    def __init__(self) -> None:
        self._seen: set[tuple[str, str, str]] = set()

    def filter_duplicates(self, postings: list[JobPostingRawData]) -> list[JobPostingRawData]:
        unique: list[JobPostingRawData] = []
        for posting in postings:
            signature = (
                posting.provider,
                posting.source_site,
                f"{posting.title}:{posting.company_name}:{posting.source_id}",
            )
            if signature in self._seen:
                continue
            self._seen.add(signature)
            unique.append(posting)
        return unique
