# AI 프롬프트 가이드

## 목적

AI 프롬프트는 코드에 직접 하드코딩하지 않고 `scripts/prompts/` 아래의 Markdown 파일로 관리합니다. 이렇게 분리하면 프롬프트 개선과 서비스 로직 변경을 독립적으로 수행할 수 있고, 포트폴리오에서도 AI 기능의 유지보수 구조를 명확히 보여줄 수 있습니다.

## 관련 파일

```text
backend/app/services/ai_service.py
backend/app/services/prompt_loader.py
scripts/prompts/
  job_summary.prompt.md
  skill_extraction.prompt.md
  job_fit_analysis.prompt.md
  resume_analysis.prompt.md
  cover_letter.prompt.md
  interview_questions.prompt.md
  company_analysis.prompt.md
  job_compare.prompt.md
```

## 동작 흐름

1. API 엔드포인트가 `AIAnalysisRequest`를 받는다.
2. `AIService.generate_response(prompt_file, **variables)`를 호출한다.
3. `PromptLoader`가 `scripts/prompts/{prompt_file}`을 읽는다.
4. `{company_name}`, `{job_title}` 같은 placeholder를 입력값으로 치환한다.
5. `AI_MODE=mock`이면 Mock 응답을 반환한다.
6. `AI_MODE=openai`이면 OpenAI API를 호출한다.
7. 모델 응답을 JSON으로 파싱한다.
8. 성공/실패 로그를 JSONL 파일에 저장한다.

## 환경변수

| 변수 | 기본값 | 설명 |
| --- | --- | --- |
| `AI_MODE` | `mock` | `mock` 또는 `openai` |
| `OPENAI_API_KEY` | 없음 | 실제 OpenAI 호출 시 필요 |
| `OPENAI_MODEL` | `gpt-4o-mini` | 사용할 모델 |
| `OPENAI_TIMEOUT` | `20` | 요청 timeout 초 |
| `OPENAI_MAX_RETRIES` | `2` | 실패 시 최대 재시도 횟수 |
| `AI_LOG_PATH` | `backend/logs/ai_calls.jsonl` | AI 호출 로그 파일 |

## PromptLoader 규칙

프롬프트 파일은 `{placeholder}` 형식의 변수를 사용할 수 있습니다.

예:

```markdown
회사명: {company_name}
직무명: {job_title}
공고 설명: {job_description}
```

서비스 호출 시 다음처럼 값을 전달합니다.

```python
service.generate_response(
    "job_summary.prompt.md",
    company_name="Example",
    job_title="Backend Engineer",
    job_description="FastAPI 기반 API 개발",
)
```

## 프롬프트 목록

| 파일 | 목적 | 주요 입력값 |
| --- | --- | --- |
| `job_summary.prompt.md` | 공고 요약 | `company_name`, `job_title`, `job_description` |
| `skill_extraction.prompt.md` | 기술스택 추출 | `company_name`, `job_title`, `job_description` |
| `job_fit_analysis.prompt.md` | 공고 적합도 분석 | `company_name`, `job_title`, `job_description`, `resume_text` |
| `resume_analysis.prompt.md` | 이력서 분석 | `resume_text` |
| `cover_letter.prompt.md` | 자기소개서 초안 | `company_name`, `job_title`, `job_description`, `resume_text` |
| `interview_questions.prompt.md` | 면접 질문 생성 | `company_name`, `job_title`, `job_description` |
| `company_analysis.prompt.md` | 기업 분석 | `company_name` |
| `job_compare.prompt.md` | 공고 비교 | `job_a_title`, `job_a_description`, `job_b_title`, `job_b_description` |

## JSON 응답 원칙

프롬프트는 반드시 JSON 형식 응답을 요구해야 합니다. 백엔드는 다음 처리를 수행합니다.

- JSON 문자열 파싱
- `json` 코드펜스 제거 후 파싱
- 응답 본문 안의 JSON 객체 추출 시도
- JSON 객체가 아니면 에러 처리

권장 응답 예:

```json
{
  "summary": "공고 요약",
  "key_responsibilities": ["업무 1", "업무 2"],
  "required_skills": ["Python", "FastAPI"]
}
```

## Mock 모드와 실제 API 모드

개발 기본값:

```env
AI_MODE=mock
```

실제 API 호출:

```env
AI_MODE=openai
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
```

Mock 모드는 프론트엔드와 API 계약을 먼저 개발하기 위한 용도입니다. 실제 API 모드는 같은 `generate_response()` 인터페이스를 유지하므로 프론트엔드 코드를 바꾸지 않고 전환할 수 있습니다.

## 에러 처리

AIService는 다음 상황을 처리합니다.

- API Key 누락
- OpenAI 패키지 누락
- timeout
- 일시적 API 실패
- 빈 응답
- JSON 파싱 실패

실패 시 API 응답의 `result`에 다음과 같은 형태로 에러 정보를 담습니다.

```json
{
  "error": "AI provider request failed",
  "details": "request timed out",
  "provider": "openai"
}
```

## 호출 로그

AI 호출 로그는 JSONL 형식으로 저장됩니다.

예:

```json
{"prompt_file":"job_summary.prompt.md","mode":"openai","success":true,"timestamp":1783330000.0,"details":{"attempt":1,"model":"gpt-4o-mini","duration_ms":842}}
```

로그에는 API Key나 원문 이력서 같은 민감한 입력값을 저장하지 않는 것을 원칙으로 합니다.

## 프롬프트 작성 체크리스트

- 출력 JSON 스키마를 명시한다.
- 사용자 입력 placeholder를 빠짐없이 사용한다.
- 모델이 설명문을 덧붙이지 않도록 JSON만 반환하라고 지시한다.
- 프롬프트 파일명은 기능을 드러내는 snake_case를 사용한다.
- 프롬프트 변경 시 관련 테스트 또는 수동 검증 결과를 남긴다.
