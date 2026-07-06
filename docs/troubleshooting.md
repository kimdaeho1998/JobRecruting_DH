# Troubleshooting

## 전체 테스트에서 `No module named 'sqlalchemy'`가 발생하는 경우

원인:

- 시스템 기본 Python 환경에 백엔드 의존성이 설치되어 있지 않음
- 프로젝트 의존성은 `backend/.venv`에 설치되어 있을 수 있음

해결:

```powershell
backend\.venv\Scripts\python.exe -m unittest discover backend\tests
```

가상환경이 없다면:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## `No module named 'app'`가 발생하는 경우

원인:

- FastAPI 앱은 `backend` 디렉터리를 기준으로 `app.*` import를 사용함
- repo root에서 테스트를 실행할 때 `backend/`가 Python path에 없으면 import 실패

해결:

- 테스트 파일에서 `backend/` 경로를 `sys.path`에 추가
- 또는 다음처럼 backend 디렉터리 기준으로 실행

```powershell
cd backend
.venv\Scripts\python.exe -m unittest discover tests
```

## OpenAI 실제 호출이 되지 않는 경우

확인할 항목:

```env
AI_MODE=openai
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
```

추가 확인:

- `backend/requirements.txt`에 `openai` 패키지가 포함되어 있는지 확인
- 가상환경에 의존성이 설치되어 있는지 확인

```powershell
backend\.venv\Scripts\python.exe -m pip show openai
```

설치:

```powershell
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## AI 응답이 Mock으로만 나오는 경우

원인:

- `AI_MODE` 기본값은 `mock`
- `.env`가 로드되지 않았거나 값이 `openai`가 아님

해결:

```env
AI_MODE=openai
OPENAI_API_KEY=your_api_key
```

서버를 재시작한 뒤 다시 호출합니다.

## AI JSON 파싱 실패

원인:

- 모델이 JSON 외 설명문을 함께 반환
- 프롬프트에 출력 스키마가 불명확함
- 응답이 배열 또는 일반 텍스트로 반환됨

해결:

- 프롬프트에 "반드시 JSON 객체만 반환" 문구 추가
- 출력 예시 JSON을 명확히 작성
- `response_format={"type": "json_object"}`를 유지

## AI 호출 로그 파일이 생성되지 않는 경우

확인할 항목:

```env
AI_LOG_PATH=backend/logs/ai_calls.jsonl
```

해결:

- 경로가 쓰기 가능한지 확인
- 서버 프로세스 권한 확인
- `backend/logs/`는 git에 포함하지 않도록 `.gitignore`에 등록

## Docker 실행 시 DB 연결 실패

확인할 항목:

- `docker compose up --build`로 실행했는지
- `db` 서비스가 먼저 정상 기동되었는지
- backend 환경변수의 host가 `localhost`가 아니라 compose 서비스명 `db`인지

Docker Compose 기준:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/jobinsight
```

로컬 실행 기준:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jobinsight
```

## 프론트엔드에서 API 호출 실패

확인할 항목:

- 백엔드가 `http://localhost:8000`에서 실행 중인지
- 프론트엔드의 API base URL이 올바른지

기본값:

```text
http://localhost:8000/api/v1
```

필요하면 `frontend/.env`에 설정합니다.

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 한글이 깨져 보이는 경우

원인:

- 파일이 UTF-8이 아닌 인코딩으로 저장되었거나 터미널 출력 인코딩이 맞지 않음

해결:

- Markdown, Python, TypeScript 파일은 UTF-8로 저장
- PowerShell 출력 인코딩 확인
- 프론트엔드 UI 텍스트를 UTF-8 기준으로 재저장

## 포트 충돌

기본 포트:

- Frontend: `3000`
- Backend: `8000`
- PostgreSQL: `5432`

이미 사용 중이면 포트를 바꾸거나 기존 프로세스를 종료합니다.

Docker Compose 포트 변경 예:

```yaml
ports:
  - "8001:8000"
```

## 테스트 실행 후 `__pycache__`가 변경 목록에 보이는 경우

원인:

- Python 실행으로 캐시 파일이 갱신됨
- 일부 캐시 파일이 git에 추적 중일 수 있음

해결:

```powershell
git status --short
git restore --source=HEAD --worktree -- backend\app\core\__pycache__\config.cpython-39.pyc
```

새 캐시 파일은 `.gitignore`의 `__pycache__/`, `*.py[cod]` 규칙으로 제외합니다.
