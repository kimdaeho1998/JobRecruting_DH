# Crawler Architecture

## Overview

This directory contains the initial structure for collecting job postings from multiple providers without implementing real site scraping yet. The design is intentionally modular so each provider can later be swapped with an actual implementation.

## Components

### 1. BaseCrawler Interface
- Defines a shared contract for all provider implementations.
- Requires `crawl(query, limit)` and `validate_config()` methods.
- Provides a simple `build_context()` hook for provider-specific metadata.

### 2. Providers
- `JobKoreaCrawler`
- `SaraminCrawler`
- `CatchCrawler`
- `WantedCrawler`
- `CompanyCrawler`

Each provider is expected to return the same `JobPostingRawData` structure, even if the underlying site HTML or API payload differs.

### 3. JobPostingRawData
Common schema for a normalized raw posting:
- provider
- source_site
- source_id
- title
- company_name
- company_id
- job_category
- location
- job_type
- experience_level
- description
- salary_range
- deadline
- source_url
- is_active
- skills
- raw_payload
- collected_at

### 4. Normalizer
- Converts provider-specific payloads into a shared format.
- Keeps raw provider payloads in `raw_payload` for future debugging or enrichment.

### 5. DeduplicationService
- Removes duplicate postings based on provider/source identity and a title/company/source-id signature.
- Can later be upgraded to use hashing or more advanced matching rules.

### 6. CrawlRunner
- Orchestrates providers.
- Runs each crawler, normalizes results, removes duplicates, and records crawl logs.

### 7. Logging Structure
Each crawl execution records:
- provider
- started_at
- finished_at
- status
- items_found
- items_new
- items_duplicates
- error
- metadata

## Planned Flow

1. A provider crawler is invoked.
2. It returns a provider-specific payload.
3. The Normalizer translates it into `JobPostingRawData`.
4. Deduplication removes duplicate candidates.
5. Crawl logs are written for traceability.

## Future Extension Points
- Add Playwright-based scraping implementations.
- Introduce a storage layer for persisting crawl results.
- Add retry and rate-limit handling.
- Support per-provider configuration and environment variables.
