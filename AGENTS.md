# AGENTS.md

## 1. 프로젝트 목적
- JobInsight AI는 AI 기반 통합 채용공고 분석 플랫폼으로, 여러 리크루팅 사이트의 채용공고를 하나의 흐름으로 수집·정규화·분석하는 것을 목표로 한다.
- 사용자는 공고 요약, 기술스택 추출, 적합도 분석, 공고 비교, 지원현황 관리를 한 곳에서 확인할 수 있어야 한다.
- 개발 과정에서는 확장성, 유지보수성, 테스트 용이성을 우선하여 구현한다.

## 2. 기술스택
- Frontend: React, TypeScript, TailwindCSS
- Backend: FastAPI, Python, SQLAlchemy
- Database: PostgreSQL
- AI: OpenAI API 예정, 현재는 Mock 구조로 설계한다.
- Crawler: Playwright 예정
- Containerization: Docker, docker-compose

## 3. 폴더 구조 규칙
- 프로젝트는 기능 중심으로 구성하되, 공통 모듈은 재사용 가능하게 분리한다.
- 권장 기본 구조:
  - frontend/: React 기반 프론트엔드 코드
  - backend/: FastAPI 기반 백엔드 코드
  - backend/app/: 애플리케이션 핵심 코드
  - backend/app/api/: API 엔드포인트
  - backend/app/services/: 비즈니스 로직
  - backend/app/repositories/: 데이터 접근 계층
  - backend/app/schemas/: 요청/응답 스키마
  - backend/app/models/: ORM 모델
  - backend/app/core/: 공통 설정, 환경변수, 예외 처리
  - backend/app/utils/: 유틸리티 함수
  - scripts/: 운영/실행 보조 스크립트
  - scripts/prompts/: AI 프롬프트 템플릿 관리
  - docs/: 프로젝트 문서
  - tests/: 테스트 코드
- 새 기능을 추가할 때는 관련 파일을 같은 도메인 하위에 배치한다.
- 공통 기능은 가능한 한 core 또는 utils로 분리한다.

## 4. 네이밍 컨벤션
- 파일명: snake_case 사용
- 디렉터리명: lowercase, 필요 시 snake_case 사용
- Python 클래스명: PascalCase
- Python 함수/변수명: snake_case
- TypeScript/React 함수명: camelCase
- TypeScript 컴포넌트명: PascalCase
- API 엔드포인트 경로: kebab-case 또는 RESTful 리소스 기반으로 명명한다.
- DB 테이블/컬럼명: snake_case 사용
- 상수명: UPPER_SNAKE_CASE 사용

## 5. API 설계 규칙
- API는 RESTful 하게 설계한다.
- 엔드포인트는 명확한 리소스 기반으로 구성한다.
- 요청/응답은 schema를 통해 명시적으로 정의한다.
- 응답 형식은 일관되게 유지한다.
- 예외 상황은 명확한 에러 응답 형식으로 반환한다.
- 클라이언트와 서버 간 계약은 문서화된 스키마를 기준으로 한다.
- 새 API는 서비스 계층을 거쳐 처리하고, 컨트롤러는 최소한의 로직만 담당한다.

## 6. Service / Repository / Schema / Model 분리 원칙
- Service: 비즈니스 로직 처리 담당
- Repository: 데이터베이스 접근 및 CRUD 처리 담당
- Schema: 요청/응답 데이터 구조 정의 담당
- Model: ORM 엔티티 또는 데이터 모델 정의 담당
- 각 계층은 역할이 분리되어야 하며, 한 계층이 다른 계층의 책임을 대신하지 않도록 한다.
- Service는 Repository를 호출하고, Repository는 Model을 직접 다룬다.
- API 계층은 비즈니스 로직을 직접 구현하지 않고 Service를 호출한다.
- Schema는 외부 계약에 사용되고, Model은 내부 데이터 저장 구조에 사용한다.

## 7. AI 프롬프트 관리 규칙
- AI 프롬프트는 반드시 scripts/prompts 아래에서 관리한다.
- 프롬프트 템플릿은 코드와 분리하여 저장한다.
- 서비스 로직 안에 프롬프트 문자열을 직접 하드코딩하지 않는다.
- 프롬프트 변경이 필요한 경우 해당 파일만 수정한다.

## 8. 환경변수 관리 규칙
- 환경변수는 .env 파일로 관리한다.
- API Key와 민감 정보는 코드에 직접 작성하지 않는다.
- .env.example 파일을 통해 필요한 환경변수 목록을 문서화한다.
- 운영/개발 환경별 설정은 분리하여 관리한다.

## 9. 테스트 코드 작성 원칙
- 기능 추가 또는 수정 시 테스트 코드를 함께 작성한다.
- 테스트는 핵심 비즈니스 로직 중심으로 작성한다.
- 외부 API, 크롤러, DB 접근 등은 가능하면 Mock 또는 Stub으로 분리하여 테스트한다.
- 테스트는 독립적으로 실행 가능해야 하며, 외부 의존성에 크게 의존하지 않아야 한다.
- 회귀 방지를 위해 주요 기능은 최소한의 단위 테스트와 통합 테스트를 포함한다.

## 10. README와 docs 문서화 규칙
- README는 프로젝트 개요, 실행 방법, 환경 설정, 주요 기능, 개발 규칙을 포함한다.
- docs 디렉터리에는 API 명세, 아키텍처, 개발 가이드, 배포 가이드 등을 정리한다.
- 문서는 코드 변경 시 함께 업데이트한다.
- 새 기능을 추가할 때는 관련 문서도 반드시 반영한다.
- 문서는 한국어와 영어를 혼용하지 않고, 팀에서 합의된 기준에 따라 작성한다.
