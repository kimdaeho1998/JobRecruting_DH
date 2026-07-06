# 시스템 아키텍처

## 전체 구조

JobInsight AI는 React 프론트엔드, FastAPI 백엔드, SQLAlchemy 기반 데이터 계층, AI 분석 서비스, 크롤러 모듈로 구성됩니다.

```text
Frontend
  React + TypeScript + TailwindCSS
  |
  | REST API
  v
Backend
  FastAPI
  |-- API Router
  |-- Service Layer
  |-- Repository Layer
  |-- Schema Layer
  |-- Model Layer
  |-- AIService
  v
Database
  PostgreSQL / SQLite

Crawler
  Provider Crawlers
  Normalizer
  DeduplicationService
```

## Frontend

위치: `frontend/`

주요 역할:

- 채용공고 목록, 상세, 북마크, 지원현황, 대시보드, 비교 화면 제공
- `frontend/src/services/api.ts`에서 백엔드 API 호출 캡슐화
- 로컬 스토리지를 사용해 북마크/비교 선택 상태 보조 저장
- Recharts 기반 통계 차트 표시

주요 화면:

- `Home`: 검색 진입과 MVP 통계 스냅샷
- `Job List`: 공고 검색과 필터링
- `Job Detail`: 공고 상세와 AI 분석 결과
- `Bookmark`: 관심 공고 목록
- `Application Board`: 지원 상태 관리
- `Dashboard`: 채용공고/지원 통계
- `Compare Jobs`: 공고 비교와 AI 비교 분석

## Backend

위치: `backend/`

백엔드는 FastAPI 기반 REST API로 구성됩니다.

```text
backend/app
  api/            API 라우터
  core/           설정, DB 연결
  models/         SQLAlchemy ORM 모델
  repositories/   데이터 접근 계층
  schemas/        Pydantic 요청/응답 스키마
  services/       비즈니스 로직
```

계층별 책임:

| 계층 | 책임 |
| --- | --- |
| API | 요청/응답 처리, 의존성 주입, HTTP 예외 처리 |
| Service | 비즈니스 로직, 여러 Repository 조합 |
| Repository | DB CRUD와 쿼리 캡슐화 |
| Schema | 외부 API 계약 정의 |
| Model | 내부 DB 테이블 구조 정의 |

## AI 처리 구조

위치:

- `backend/app/services/ai_service.py`
- `backend/app/services/prompt_loader.py`
- `scripts/prompts/`

흐름:

1. API에서 AI 분석 요청을 받는다.
2. `AIService.generate_response()`가 프롬프트 파일명과 입력값을 받는다.
3. `PromptLoader`가 Markdown 프롬프트 템플릿을 로드한다.
4. placeholder에 입력값을 주입한다.
5. `AI_MODE=mock`이면 Mock 응답을 반환한다.
6. `AI_MODE=openai`이면 OpenAI API를 호출한다.
7. 응답을 JSON으로 파싱하고 호출 로그를 JSONL로 저장한다.

## 데이터베이스

기본 운영 DB는 PostgreSQL입니다. 로컬 테스트에서는 SQLite도 사용할 수 있도록 `DATABASE_URL`을 환경변수로 분리했습니다.

주요 엔티티:

- Company
- JobPosting
- Skill
- JobSkill
- User
- Bookmark
- Application
- Resume
- ResumeAnalysis
- CompanyFollow
- Notification

자세한 관계는 [erd.md](erd.md)를 참고합니다.

## Crawler

위치: `crawler/`

크롤러는 실제 사이트별 구현을 바로 코드에 섞지 않고 Provider 패턴으로 분리했습니다.

- `BaseCrawler`: 모든 크롤러의 공통 인터페이스
- `providers/`: JobKorea, Saramin, Catch, Wanted, Company 크롤러
- `Normalizer`: 사이트별 데이터를 공통 구조로 변환
- `DeduplicationService`: 중복 공고 제거
- `CrawlRunner`: 수집 실행 흐름 조율

자세한 내용은 [crawler-architecture.md](crawler-architecture.md)를 참고합니다.

## 환경 설정

주요 환경변수:

| 변수 | 설명 |
| --- | --- |
| `DATABASE_URL` | DB 연결 문자열 |
| `AI_MODE` | `mock` 또는 `openai` |
| `OPENAI_API_KEY` | OpenAI API Key |
| `OPENAI_MODEL` | 사용할 OpenAI 모델 |
| `OPENAI_TIMEOUT` | OpenAI 요청 timeout |
| `OPENAI_MAX_RETRIES` | OpenAI 재시도 횟수 |
| `AI_LOG_PATH` | AI 호출 로그 JSONL 파일 경로 |

## 배포 구조

`docker-compose.yml`은 다음 서비스를 정의합니다.

- `db`: PostgreSQL 16
- `backend`: FastAPI API 서버
- `frontend`: React/Vite 프론트엔드

개발 환경에서는 Docker Compose 또는 로컬 venv/npm 실행 방식을 선택할 수 있습니다.
