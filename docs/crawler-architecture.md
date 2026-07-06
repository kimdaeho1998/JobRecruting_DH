# 크롤러 아키텍처

## 목적

크롤러 모듈은 여러 채용 플랫폼에서 수집한 공고 데이터를 하나의 공통 구조로 정규화하기 위해 설계되었습니다. 현재는 실제 사이트 스크래핑보다 확장 가능한 구조를 먼저 마련한 단계이며, 이후 Playwright 기반 Provider 구현을 붙일 수 있습니다.

## 디렉터리 구조

```text
crawler/
  core/
    base_crawler.py
    crawl_runner.py
    deduplication_service.py
    models.py
    normalizer.py
  providers/
    job_korea_crawler.py
    saramin_crawler.py
    catch_crawler.py
    wanted_crawler.py
    company_crawler.py
```

## 핵심 컴포넌트

### BaseCrawler

모든 사이트별 크롤러가 따라야 하는 공통 인터페이스입니다.

주요 책임:

- `crawl(query, limit)` 메서드 정의
- `validate_config()`로 사이트별 설정 검증
- Provider 메타데이터를 구성하는 hook 제공

### Provider Crawlers

사이트별 수집 로직을 담당합니다.

현재 준비된 Provider:

- `JobKoreaCrawler`
- `SaraminCrawler`
- `CatchCrawler`
- `WantedCrawler`
- `CompanyCrawler`

각 Provider는 사이트별 HTML, API, 페이지네이션, 로그인 여부 등이 달라도 최종적으로 같은 데이터 구조를 반환해야 합니다.

### JobPostingRawData

크롤러가 반환하는 공통 원시 데이터 모델입니다.

주요 필드:

- `provider`
- `source_site`
- `source_id`
- `title`
- `company_name`
- `company_id`
- `job_category`
- `location`
- `job_type`
- `experience_level`
- `description`
- `salary_range`
- `deadline`
- `source_url`
- `is_active`
- `skills`
- `raw_payload`
- `collected_at`

### Normalizer

Provider별 데이터 형식 차이를 공통 구조로 변환합니다.

예:

- 사이트별 회사명 필드명 통일
- 마감일 문자열을 날짜 타입으로 변환
- 기술스택 문자열을 리스트로 분리
- 원본 payload를 `raw_payload`에 보존

### DeduplicationService

중복 공고를 제거합니다.

현재 기준:

- Provider와 source identity
- 회사명, 제목, source id 기반 signature

향후 개선:

- URL canonicalization
- 제목 유사도 기반 fuzzy matching
- 회사명 alias 매핑
- 해시 기반 변경 감지

### CrawlRunner

크롤링 실행 흐름을 조율합니다.

흐름:

1. Provider 목록을 순회한다.
2. 각 Provider의 설정을 검증한다.
3. 공고 데이터를 수집한다.
4. Normalizer로 공통 구조로 변환한다.
5. DeduplicationService로 중복을 제거한다.
6. 실행 로그를 기록한다.

## 수집 로그

크롤링 실행마다 다음 정보를 남기는 구조를 목표로 합니다.

- `provider`
- `started_at`
- `finished_at`
- `status`
- `items_found`
- `items_new`
- `items_duplicates`
- `error`
- `metadata`

## 장애 대응 전략

- Provider별 timeout과 retry를 분리
- 사이트별 rate limit 설정
- 실패한 Provider가 있어도 전체 Runner는 가능한 범위에서 계속 진행
- 원본 payload 저장으로 디버깅 가능성 확보
- 사이트 구조 변경 시 Provider 단위로 수정

## 향후 구현 계획

- Playwright 기반 실제 수집 구현
- Provider별 환경변수와 설정 파일 추가
- 크롤링 결과 DB 저장
- 증분 수집과 변경 감지
- 스케줄러 연동
- 크롤링 로그 API와 관리자 화면 추가
