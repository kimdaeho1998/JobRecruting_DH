# Architecture

## 1. 시스템 아키텍처
JobInsight AI는 프론트엔드, 백엔드, 데이터베이스, AI 분석 모듈로 구성되는 모듈형 웹 애플리케이션이다.

초기 MVP는 다음 구조로 설계한다.

- Frontend: React + TypeScript + TailwindCSS
- Backend: FastAPI + Python + SQLAlchemy
- Database: PostgreSQL
- AI Processing: OpenAI API 연동 구조, 초기에는 Mock 응답 사용
- Deployment: Docker + docker-compose

## 2. 서비스 구성 요소
### Frontend
- 대시보드 페이지
- 공고 상세 페이지
- 비교 페이지
- 지원현황 관리 페이지
- 공통 레이아웃 및 UI 컴포넌트

### Backend
- API 엔드포인트 제공
- 공고/분석/지원현황 비즈니스 로직 처리
- AI 분석 요청 처리
- 데이터베이스 접근 및 저장

### Data Layer
- 공고 정보 저장
- 사용자 지원 상태 저장
- 분석 결과 저장
- Mock Data 관리

## 3. DB 테이블 초안
### users
- id
- email
- password_hash
- name
- created_at
- updated_at

### job_postings
- id
- title
- company_name
- location
- job_type
- experience_level
- description
- source_name
- source_url
- created_at
- updated_at

### job_analysis_results
- id
- job_posting_id
- summary
- extracted_skills
- suitability_score
- analysis_status
- created_at
- updated_at

### application_statuses
- id
- user_id
- job_posting_id
- status
- applied_at
- note
- created_at
- updated_at

### comparison_sessions
- id
- user_id
- name
- created_at
- updated_at

### comparison_items
- id
- comparison_session_id
- job_posting_id
- created_at

## 4. API 엔드포인트 초안
### 공고 관련
- GET /api/v1/job-postings
- GET /api/v1/job-postings/{id}
- GET /api/v1/job-postings/{id}/analysis

### 비교 관련
- GET /api/v1/comparisons
- POST /api/v1/comparisons
- GET /api/v1/comparisons/{id}

### 지원현황 관련
- GET /api/v1/applications
- POST /api/v1/applications
- PATCH /api/v1/applications/{id}

### 사용자 관련
- POST /api/v1/auth/register
- POST /api/v1/auth/login

## 5. 프론트엔드 페이지 구성
- 홈/대시보드 페이지
- 공고 목록 페이지
- 공고 상세 페이지
- 비교 페이지
- 지원현황 페이지
- 설정/프로필 페이지

## 6. 초기 구현 방향
- 백엔드 API는 Mock Data를 반환하는 구조로 먼저 구현한다.
- AI 분석 결과는 실제 OpenAI 호출 대신 사전 정의된 Mock 응답으로 대체한다.
- 프론트엔드는 API 응답 형태를 기준으로 UI를 먼저 구성한다.
- 이후 실제 크롤링 및 AI 연동 단계에서 구조를 확장한다.
