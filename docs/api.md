# API 명세

## 기본 정보

- Base URL: `http://localhost:8000/api/v1`
- Swagger UI: `http://localhost:8000/docs`
- 응답 형식: JSON
- 기본 사용자 ID: MVP에서는 `user_id=1`을 기본값으로 사용

## Job Postings

### GET `/job-postings`

채용공고 목록을 조회합니다.

Query Parameters:

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `q` | string | 제목, 설명, 회사명 통합 검색 |
| `job_category` | string | 직무 필터 |
| `company_name` | string | 회사명 필터 |
| `location` | string | 지역 필터 |
| `experience_level` | string | 경력 조건 필터 |
| `skill` | string | 기술스택 필터 |
| `deadline_from` | date | 마감일 시작 |
| `deadline_to` | date | 마감일 종료 |
| `is_active` | boolean | 활성 공고 여부 |
| `offset` | integer | 페이지 offset |
| `limit` | integer | 조회 개수, 최대 100 |

Response: `JobPostingSummary[]`

### GET `/job-postings/search`

검색어가 필수인 공고 검색 API입니다. 필터 구조는 `/job-postings`와 동일합니다.

### GET `/job-postings/{job_posting_id}`

채용공고 상세 정보를 조회합니다.

Response: `JobPostingDetail`

## Catalog

### GET `/companies`

회사 목록을 조회합니다.

Query Parameters:

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `name` | string | 회사명 검색 |

### GET `/skills`

기술스택 목록을 조회합니다.

Query Parameters:

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `name` | string | 기술명 검색 |

## Bookmarks

### POST `/bookmarks`

관심 공고를 등록합니다.

Request:

```json
{
  "user_id": 1,
  "job_posting_id": 10
}
```

Response: `BookmarkRead`

### DELETE `/bookmarks`

관심 공고를 삭제합니다.

Query Parameters:

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `user_id` | integer | 사용자 ID, 기본값 1 |
| `job_posting_id` | integer | 공고 ID |

Response: `204 No Content`

## Applications

### GET `/applications`

사용자의 지원현황 목록을 조회합니다.

Query Parameters:

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `user_id` | integer | 사용자 ID, 기본값 1 |

Response: `ApplicationListItem[]`

### POST `/applications`

지원현황을 등록합니다.

Request:

```json
{
  "user_id": 1,
  "job_posting_id": 10,
  "status": "지원 예정",
  "notes": "포트폴리오 보강 후 지원",
  "applied_at": null,
  "deadline": "2026-07-31"
}
```

Response: `ApplicationRead`

### PATCH `/applications/{application_id}`

지원현황을 수정합니다.

Request:

```json
{
  "status": "서류 합격",
  "notes": "코딩테스트 일정 확인"
}
```

Response: `ApplicationRead`

## Company Follows

### POST `/company-follows`

관심 기업을 등록합니다.

Request:

```json
{
  "user_id": 1,
  "company_id": 3
}
```

Response: `CompanyFollowRead`

### DELETE `/company-follows`

관심 기업을 삭제합니다.

Query Parameters:

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `user_id` | integer | 사용자 ID, 기본값 1 |
| `company_id` | integer | 회사 ID |

Response: `204 No Content`

## Dashboard

### GET `/dashboard/stats`

대시보드 통계를 조회합니다.

Response:

```json
{
  "total_job_postings": 100,
  "active_job_postings": 92,
  "new_job_postings": 12,
  "deadline_soon_job_postings": 8,
  "total_companies": 30,
  "total_skills": 45,
  "total_bookmarks": 5,
  "total_applications": 7,
  "total_company_follows": 2,
  "applications_by_status": {
    "지원 예정": 2,
    "지원 완료": 3
  },
  "completed_applications": 3,
  "top_skills": [{ "name": "Python", "value": 15 }],
  "job_count_by_location": [{ "name": "Seoul", "value": 40 }],
  "job_count_by_category": [{ "name": "Backend", "value": 20 }],
  "application_status_ratio": [{ "name": "지원 완료", "value": 42.9 }]
}
```

## AI

### POST `/ai/analyze`

프롬프트 파일명을 직접 지정해 AI 분석을 실행합니다.

Request:

```json
{
  "prompt_file": "job_summary.prompt.md",
  "company_name": "Example",
  "job_title": "Backend Engineer",
  "job_description": "FastAPI 기반 API 개발"
}
```

Response:

```json
{
  "prompt_file": "job_summary.prompt.md",
  "result": {
    "summary": "공고 요약",
    "key_responsibilities": ["API 개발"],
    "required_skills": ["Python", "FastAPI"]
  }
}
```

### AI 전용 엔드포인트

| Method | Path | 설명 | Prompt |
| --- | --- | --- | --- |
| POST | `/ai/summary` | 공고 요약 | `job_summary.prompt.md` |
| POST | `/ai/skills` | 기술스택 추출 | `skill_extraction.prompt.md` |
| POST | `/ai/fit` | 공고 적합도 분석 | `job_fit_analysis.prompt.md` |
| POST | `/ai/resume` | 이력서 분석 | `resume_analysis.prompt.md` |
| POST | `/ai/cover-letter` | 자기소개서 초안 | `cover_letter.prompt.md` |
| POST | `/ai/interview-questions` | 면접 질문 생성 | `interview_questions.prompt.md` |
| POST | `/ai/company-analysis` | 기업 분석 | `company_analysis.prompt.md` |
| POST | `/ai/compare` | 공고 비교 | `job_compare.prompt.md` |

## 주요 응답 스키마

### JobPostingSummary

```json
{
  "id": 1,
  "company_id": 1,
  "company_name": "Example",
  "title": "Backend Engineer",
  "job_category": "Backend",
  "location": "Seoul",
  "job_type": "Full-time",
  "experience_level": "3년 이상",
  "salary_range": "협의",
  "deadline": "2026-07-31",
  "source_site": "Mock",
  "source_url": "https://example.com/jobs/1",
  "is_active": true,
  "skills": ["Python", "FastAPI"]
}
```

### AIAnalysisRequest

```json
{
  "prompt_file": "job_summary.prompt.md",
  "company_name": "Example",
  "job_title": "Backend Engineer",
  "job_description": "공고 본문",
  "resume_text": "이력서 본문",
  "job_a_title": "A 공고",
  "job_a_description": "A 설명",
  "job_b_title": "B 공고",
  "job_b_description": "B 설명"
}
```
