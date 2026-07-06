# 개발 로드맵

## 현재 상태 요약

현재 프로젝트는 MVP의 핵심 구조가 구현된 상태입니다.

- React 기반 프론트엔드 워크스페이스 구현
- FastAPI REST API 구현
- SQLAlchemy ORM 모델과 Repository/Service 계층 구성
- 채용공고, 북마크, 지원현황, 회사 관심, 대시보드 API 구현
- AIService의 Mock/OpenAI 전환 구조 구현
- 프롬프트 파일 기반 PromptLoader 구현
- Provider 기반 크롤러 골격 구현
- unittest 기반 서비스 테스트 작성

## Phase 1. 프로젝트 기획 및 구조 설계

상태: 완료

- 프로젝트 목표와 문제 정의
- 기술스택 선정
- 폴더 구조 정의
- AGENTS.md, README, docs 기반 협업 규칙 정리
- Docker Compose 기본 구조 작성

## Phase 2. 백엔드 MVP

상태: 완료

- FastAPI 앱 구성
- DB 설정과 SQLAlchemy 모델 작성
- Pydantic Schema 작성
- Repository 계층 구성
- Service 계층 구성
- REST API 라우트 구현
- 시드 데이터 생성 스크립트 작성

주요 결과:

- 공고 조회/검색 API
- 회사/기술스택 catalog API
- 북마크 API
- 지원현황 API
- 회사 관심 API
- 대시보드 통계 API

## Phase 3. 프론트엔드 MVP

상태: 완료

- Vite + React + TypeScript 구성
- TailwindCSS 스타일 적용
- API client 작성
- 공고 목록/상세 화면 구현
- 북마크 화면 구현
- 지원현황 보드 구현
- 대시보드 차트 구현
- 공고 비교 화면 구현

## Phase 4. AI 분석 구조

상태: 완료

- Mock AIService 구현
- OpenAI API 호출 구조 추가
- `.env` 기반 API Key 관리
- `AI_MODE=mock|openai` 전환
- PromptLoader 기반 프롬프트 파일 로드
- placeholder 입력값 주입
- JSON 응답 파싱
- Retry, Timeout, 에러 처리
- AI 호출 로그 저장
- AI 서비스 단위 테스트 작성

## Phase 5. 크롤러 구조 설계

상태: 설계/골격 구현

- BaseCrawler 인터페이스
- 사이트별 Provider 골격
- 공통 raw data 모델
- Normalizer
- DeduplicationService
- CrawlRunner

다음 작업:

- Playwright 도입
- 사이트별 실제 수집 로직 구현
- 크롤링 결과 저장 계층 연결
- 실패/재시도/속도 제한 정책 추가

## Phase 6. 운영 품질 개선

상태: 예정

- 인증/인가 구현
- 사용자별 데이터 분리
- AI 분석 결과 저장
- API 에러 응답 표준화
- 테스트 커버리지 확대
- CI 파이프라인 구성
- 배포 환경 분리
- 로그/모니터링 구축

## Phase 7. 포트폴리오 완성도 개선

상태: 진행 가능

- 프론트엔드 한글 텍스트 인코딩 정리
- 주요 화면 스크린샷 추가
- Swagger API 캡처 추가
- ERD 이미지 추가
- 크롤러 동작 예시 추가
- 실제 OpenAI 분석 결과 샘플 추가
- 배포 URL 또는 데모 영상 추가

## 우선순위

1. 깨진 한글 UI 텍스트 정리
2. `.env.example`과 Docker 환경변수 정합성 확인
3. 실제 OpenAI 모드 smoke test
4. 크롤러 Provider 1개 실제 구현
5. 포트폴리오용 화면 캡처와 데모 시나리오 작성

## 성공 기준

- 사용자가 공고 검색부터 지원 상태 관리까지 하나의 흐름으로 사용할 수 있다.
- AI 분석 기능이 Mock/실제 API 양쪽에서 같은 API 계약으로 동작한다.
- 새로운 채용 사이트를 Provider 단위로 추가할 수 있다.
- 문서만 읽어도 프로젝트의 문제 정의, 설계 이유, 구현 범위, 확장 방향을 이해할 수 있다.
