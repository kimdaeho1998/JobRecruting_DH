# JobInsight AI

JobInsight AI는 AI 기반 통합 채용공고 분석 플랫폼의 기본 구조를 담은 프로젝트입니다.

## 프로젝트 구조
- frontend/: React + TypeScript + TailwindCSS 기반 프론트엔드
- backend/: FastAPI 기반 백엔드 API
- crawler/: 크롤링 모듈용 디렉터리
- scripts/: 운영/실행 보조 스크립트
- docs/: 프로젝트 설계 문서
- docker/: 컨테이너 관련 설정 디렉터리

## 실행 방법

### 1. 환경 변수 설정
```bash
cp .env.example .env
```

### 2. Docker로 실행
```bash
docker compose up --build
```

- 프론트엔드: http://localhost:3000
- 백엔드: http://localhost:8000
- PostgreSQL: localhost:5432

### 3. 로컬 개발 실행

#### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows는 .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 현재 상태
- 기본 프론트엔드 화면 구성 완료
- FastAPI 기본 API 엔드포인트 구성 완료
- PostgreSQL 연결 준비 완료
- Docker Compose 기본 구성 완료
- 상세 기능 구현은 이후 단계에서 진행
