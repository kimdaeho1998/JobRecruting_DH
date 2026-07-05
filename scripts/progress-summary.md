# JobInsight AI 진행 상황 요약

## 1. 프로젝트 개요
JobInsight AI는 여러 채용 사이트의 공고를 수집·정규화·분석해 사용자가 한 곳에서 비교·관리할 수 있도록 돕는 플랫폼입니다.

## 2. 현재까지 구현된 내용

### 2.1 프로젝트 문서화
- AGENTS.md 작성
- 프로젝트 개요 문서 작성
- 아키텍처 문서 작성
- 개발 로드맵 문서 작성
- ERD 문서 작성

### 2.2 프론트엔드 기본 구조
- React + TypeScript + Vite + TailwindCSS 기반 초기 프론트엔드 구성
- 기본 앱 진입 컴포넌트 구현
- 스타일 초기 설정 완료
- 프론트엔드 빌드 검증 완료

### 2.3 백엔드 기본 구조
- FastAPI 기반 API 엔트리포인트 구성
- 헬스 체크 엔드포인트 구현
- 환경 변수 설정 모듈 구성
- 기본 서비스 계층 구조 확보

### 2.4 데이터 모델 계층
- SQLAlchemy ORM 모델 구현
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
- Pydantic 스키마 구현
- Repository 계층 기본 구현

### 2.5 Mock 데이터 시딩
- 개발/테스트용 Mock 채용공고 시드 스크립트 구현
- 최소 100개 채용공고 생성 로직 구현
- 직무 카테고리 포함
  - AI 개발자
  - 백엔드 개발자
  - 프론트엔드 개발자
  - 데이터 엔지니어
  - 데이터 분석가
  - MES 개발자
  - 기획자
- 회사명, 공고명, 지역, 경력, 기술스택, 마감일, 출처 사이트, 상세 내용 포함
- 시드 스크립트로 DB 적재 가능

## 3. 현재 사용 가능한 실행 방식

### 3.1 시드 실행
```powershell
.\backend\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, ''); from scripts.seed.seed_jobs import seed_job_postings; seed_job_postings(count=100, database_url='sqlite:///./jobinsight_test.db')"
```

### 3.2 백엔드 실행
```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3.3 프론트엔드 실행
```powershell
cd frontend
npm run dev
```

## 4. 검증 결과
다음 항목은 실제 실행을 통해 확인되었습니다.
- 프론트엔드 빌드 성공
- 백엔드 헬스 체크 응답 확인
- ORM 모델 import 성공
- Mock 시드 스크립트 실행 성공
- DB에 채용공고 100건 적재 확인

## 5. 현재 상태 평가
- 기본 프로젝트 골격은 완성 단계에 있습니다.
- 데이터 모델과 시딩 로직은 동작 중입니다.
- 다음 단계로는 API 엔드포인트 구현, DB 연결/마이그레이션, 실제 크롤러 연동 준비가 가능합니다.

## 6. 다음 권장 작업
1. API 엔드포인트 구현
2. PostgreSQL 연결 구성
3. Alembic 마이그레이션 설정
4. 실제 크롤링 로직 연동 준비
5. 테스트 코드 확장
