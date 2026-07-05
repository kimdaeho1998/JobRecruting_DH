# Codex 이어서 진행용 작업 안내

## 1. 현재 상태 요약
이 저장소는 JobInsight AI의 MVP 초기 구조까지 구현된 상태입니다.

- 프론트엔드: React + TypeScript + Vite + TailwindCSS
- 백엔드: FastAPI + SQLAlchemy + Pydantic
- 데이터베이스: SQLAlchemy 모델 및 시드 데이터 처리 구성
- Mock 데이터: 100개 채용공고 시드 데이터 생성 가능

## 2. 이미 완료된 작업
- 프로젝트 규칙 문서 작성
- 아키텍처/로드맵/ERD 문서 작성
- 프론트엔드 기본 화면 구성
- 백엔드 기본 API 진입점 구성
- ORM 모델 구성
- Pydantic 스키마 구성
- Repository 계층 구성
- Mock 공고 시드 스크립트 구성
- 시드 데이터를 DB에 삽입하는 흐름 검증 완료

## 3. 바로 이어서 진행할 작업 권장 순서

### 3.1 API 엔드포인트 구현
다음 엔드포인트를 우선 구현하는 것을 권장합니다.
- GET /api/v1/job-postings
- GET /api/v1/job-postings/{id}
- GET /api/v1/companies
- GET /api/v1/skills
- POST /api/v1/bookmarks
- GET /api/v1/applications

### 3.2 DB 연결 및 환경 구성
- PostgreSQL 사용을 가정하고 DATABASE_URL 설정
- 개발/테스트용 SQLite와 PostgreSQL을 분리 가능하도록 구성
- .env.example 및 .env 사용 흐름 정리

### 3.3 마이그레이션 구성
- Alembic 또는 간단한 초기화 스크립트로 테이블 생성 흐름 정리
- 시드 실행과 마이그레이션을 분리

### 3.4 실제 크롤링 준비
- 현재는 Mock 데이터만 사용
- 향후 크롤링 모듈은 다음 구조로 확장 가능
  - crawler/scraper.py
  - crawler/parser.py
  - crawler/models.py

## 4. 구현 우선순위
1. API 레이어 추가
2. 서비스 레이어와 repository 연결
3. DB 연결 안정화
4. 테스트 코드 확장
5. 실제 크롤링 모듈 설계

## 5. 참고 파일
- [backend/app/main.py](backend/app/main.py)
- [backend/app/models/__init__.py](backend/app/models/__init__.py)
- [backend/app/schemas/__init__.py](backend/app/schemas/__init__.py)
- [backend/app/repositories/__init__.py](backend/app/repositories/__init__.py)
- [scripts/seed/seed_jobs.py](scripts/seed/seed_jobs.py)

## 6. Codex에게 전달할 핵심 메시지
다음 문장을 Codex에 전달하면 작업 이어서 진행이 쉬워집니다.

> JobInsight AI 프로젝트의 MVP 초기 구조가 이미 구현되어 있습니다. 프론트엔드와 백엔드 기본 골격, SQLAlchemy 모델, Pydantic 스키마, Repository 계층, Mock 채용공고 100건 시드 스크립트까지 완료되었습니다. 이제 API 엔드포인트와 DB 연결 흐름을 구현하는 단계로 이어서 진행해 주세요.
