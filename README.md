# JobInsight AI

## 프로젝트 소개

JobInsight AI는 여러 채용 플랫폼에 흩어진 채용공고를 수집, 정규화, 분석하고 사용자의 지원 흐름까지 관리하는 AI 기반 채용공고 분석 플랫폼입니다. 포트폴리오 관점에서는 단순 CRUD를 넘어 데이터 수집 구조, REST API, 프론트엔드 워크스페이스, AI 프롬프트 관리, 테스트 가능한 서비스 계층을 함께 설계한 프로젝트입니다.

## 문제 정의

채용 준비 과정에서는 공고가 여러 사이트에 분산되어 있어 비교와 관리가 번거롭습니다. 공고마다 기술스택, 경력 조건, 업무 범위의 표현 방식도 달라 핵심 정보를 빠르게 파악하기 어렵고, 관심 공고와 지원 상태를 별도 스프레드시트로 관리하는 경우가 많습니다.

JobInsight AI는 이 문제를 다음 흐름으로 해결하려고 합니다.

- 여러 소스의 채용공고를 공통 스키마로 정규화
- 기술스택, 마감일, 직무, 회사 정보를 기준으로 탐색
- AI 기반 공고 요약, 기술스택 추출, 적합도 분석, 공고 비교 제공
- 북마크, 지원 상태, 대시보드로 개인 채용 파이프라인 관리

## 주요 기능

- 채용공고 목록 조회, 검색, 필터링
- 채용공고 상세 조회 및 기술스택 표시
- 북마크 등록 및 해제
- 지원 상태 등록, 수정, 보드 형태 관리
- 회사 관심 등록
- 대시보드 통계: 전체 공고, 신규 공고, 마감 임박 공고, 기술스택 빈도, 지역/직무 분포, 지원 상태 비율
- AI 분석: 공고 요약, 기술스택 추출, 적합도 분석, 이력서 분석, 자기소개서 초안, 면접 질문, 기업 분석, 공고 비교
- Mock AI 모드와 실제 OpenAI API 모드 전환
- 크롤러 확장을 위한 Provider, Normalizer, Deduplication 구조

## 기술스택

| 영역 | 기술 |
| --- | --- |
| Frontend | React, TypeScript, Vite, TailwindCSS, Recharts |
| Backend | FastAPI, Python, SQLAlchemy, Pydantic |
| Database | PostgreSQL, 로컬 테스트용 SQLite |
| AI | OpenAI API 연동 구조, Mock 모드, 프롬프트 파일 관리 |
| Crawler | Playwright 확장 예정, Provider 기반 크롤러 구조 |
| Infra | Docker, docker-compose |
| Test | unittest, 서비스 계층 중심 테스트 |

## 시스템 아키텍처

```text
사용자
  |
  v
React Frontend
  |  REST API
  v
FastAPI Backend
  |-- API Layer
  |-- Service Layer
  |-- Repository Layer
  |-- AIService + PromptLoader
  v
PostgreSQL / SQLite

Crawler Layer
  |-- Provider Crawlers
  |-- Normalizer
  |-- DeduplicationService
  v
공통 채용공고 데이터 모델
```

자세한 설계는 [docs/architecture.md](docs/architecture.md), API 명세는 [docs/api.md](docs/api.md), ERD는 [docs/erd.md](docs/erd.md)를 참고하세요.

## 실행 방법

### 1. 환경변수 설정

```bash
cp .env.example .env
```

기본값은 AI Mock 모드입니다.

```env
AI_MODE=mock
```

실제 OpenAI API를 사용하려면 다음처럼 변경합니다.

```env
AI_MODE=openai
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
```

### 2. Docker 실행

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 3. 로컬 개발 실행

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

### 4. 테스트 실행

```powershell
backend\.venv\Scripts\python.exe -m unittest discover backend\tests
```

## 주요 화면 설명

- Home: 프로젝트 요약, 검색 진입, MVP 통계 스냅샷
- Job List: 공고 목록, 검색어/직무/회사/지역/경력/기술스택/마감일 필터
- Job Detail: 공고 상세, 북마크, 비교 추가, 지원 상태 변경, AI 분석 결과
- Bookmark: 저장한 관심 공고 목록
- Application Board: 지원 상태별 칸반형 보드
- Dashboard: 공고/지원 현황 통계 및 차트
- Compare Jobs: 선택한 공고 비교와 AI 비교 분석 결과

## AI 기능 설명

AI 기능은 `backend/app/services/ai_service.py`에서 담당합니다.

- `PromptLoader`가 `scripts/prompts` 아래의 프롬프트 템플릿을 로드
- `{company_name}`, `{job_title}`, `{job_description}` 같은 placeholder에 입력값 주입
- `AI_MODE=mock`이면 개발용 Mock 응답 반환
- `AI_MODE=openai`이면 OpenAI API 호출
- JSON 응답 파싱, 코드펜스 제거, 에러 응답 처리
- Retry, Timeout, 호출 로그(JSONL) 저장
- API Key는 `.env`의 `OPENAI_API_KEY`에서만 읽음

프롬프트 관리 방식은 [docs/ai-prompt-guide.md](docs/ai-prompt-guide.md)에 정리했습니다.

## 향후 개선 방향

- 실제 채용 사이트별 Playwright 크롤러 구현
- 크롤링 결과 DB 저장 및 증분 수집
- 사용자 인증과 개인별 데이터 분리
- AI 분석 결과 저장 및 재사용
- 이력서 기반 개인화 추천 고도화
- 테스트 커버리지 확대 및 CI 도입
- 배포 환경 분리와 운영 로그/모니터링 구축

## 포트폴리오 관점에서 강조할 점

- 기능 중심 폴더 구조와 Service/Repository/Schema/Model 계층 분리
- Mock에서 실제 OpenAI API로 전환 가능한 AI 서비스 설계
- 프롬프트를 코드 밖에서 관리하는 구조
- 크롤러를 Provider, Normalizer, Deduplication으로 분리한 확장 설계
- 대시보드와 지원 상태 관리까지 포함한 end-to-end 사용자 흐름
- unittest 기반 회귀 테스트와 테스트 가능한 서비스 구조
