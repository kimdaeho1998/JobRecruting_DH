# ERD

## 개요

JobInsight AI의 데이터 모델은 채용공고 탐색, 기술스택 분석, 사용자 지원 상태 관리, 이력서 분석 확장을 기준으로 설계되었습니다.

## 엔티티 관계 요약

```text
Company 1 ── N JobPosting
JobPosting N ── M Skill       (via JobSkill)
User 1 ── N Bookmark
User 1 ── N Application
User 1 ── N Resume
Resume 1 ── N ResumeAnalysis
JobPosting 1 ── N ResumeAnalysis
User 1 ── N CompanyFollow
User 1 ── N Notification
```

## 주요 테이블

### companies

기업 정보를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `name` | 회사명 |
| `website` | 회사 웹사이트 |
| `industry` | 산업군 |
| `description` | 회사 설명 |
| `created_at`, `updated_at` | 생성/수정 시각 |

### job_postings

채용공고 정보를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `company_id` | companies FK |
| `title` | 공고 제목 |
| `job_category` | 직무 카테고리 |
| `location` | 근무 지역 |
| `job_type` | 고용 형태 |
| `experience_level` | 경력 조건 |
| `description` | 공고 상세 설명 |
| `salary_range` | 급여 범위 |
| `deadline` | 마감일 |
| `source_site` | 출처 사이트 |
| `source_url` | 원문 URL |
| `is_active` | 활성 공고 여부 |
| `created_at`, `updated_at` | 생성/수정 시각 |

### skills

기술스택 마스터 데이터를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `name` | 기술명 |
| `category` | 기술 카테고리 |
| `created_at`, `updated_at` | 생성/수정 시각 |

### job_skills

공고와 기술스택의 다대다 관계를 연결합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `job_posting_id` | job_postings FK |
| `skill_id` | skills FK |
| `created_at`, `updated_at` | 생성/수정 시각 |

제약:

- `job_posting_id`, `skill_id` 조합은 유일해야 합니다.

### users

사용자 정보를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `email` | 이메일 |
| `password_hash` | 비밀번호 해시 |
| `full_name` | 사용자 이름 |
| `is_active` | 활성 사용자 여부 |
| `created_at`, `updated_at` | 생성/수정 시각 |

### bookmarks

사용자의 관심 공고를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `user_id` | users FK |
| `job_posting_id` | job_postings FK |
| `created_at`, `updated_at` | 생성/수정 시각 |

제약:

- 사용자와 공고 조합은 유일해야 합니다.

### applications

사용자의 지원 상태를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `user_id` | users FK |
| `job_posting_id` | job_postings FK |
| `status` | 지원 상태 |
| `applied_at` | 지원일 |
| `deadline` | 사용자 관리용 마감일 |
| `notes` | 메모 |
| `created_at`, `updated_at` | 생성/수정 시각 |

제약:

- 사용자와 공고 조합은 유일해야 합니다.

### resumes

사용자 이력서 데이터를 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `user_id` | users FK |
| `title` | 이력서 제목 |
| `content` | 이력서 본문 |
| `file_name` | 업로드 파일명 |
| `created_at`, `updated_at` | 생성/수정 시각 |

### resume_analyses

이력서와 공고를 기준으로 한 AI 분석 결과를 저장할 수 있는 확장 테이블입니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `resume_id` | resumes FK |
| `job_posting_id` | job_postings FK, nullable |
| `score` | 적합도 점수 |
| `summary` | 분석 요약 |
| `recommendations` | 개선 추천 |
| `created_at`, `updated_at` | 생성/수정 시각 |

### company_follows

사용자가 관심 기업을 저장합니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `user_id` | users FK |
| `company_id` | companies FK |
| `created_at`, `updated_at` | 생성/수정 시각 |

### notifications

향후 마감 알림, 관심 기업 신규 공고 알림 등을 저장하기 위한 테이블입니다.

| 컬럼 | 설명 |
| --- | --- |
| `id` | PK |
| `user_id` | users FK |
| `notification_type` | 알림 유형 |
| `title` | 제목 |
| `body` | 본문 |
| `is_read` | 읽음 여부 |
| `related_type` | 관련 리소스 유형 |
| `related_id` | 관련 리소스 ID |
| `created_at`, `updated_at` | 생성/수정 시각 |

## 인덱스와 제약 조건

- `companies.name`: 회사명 검색
- `job_postings.company_id`: 회사별 공고 조회
- `job_postings.title`: 제목 검색
- `skills.name`: 기술스택 검색 및 중복 방지
- `users.email`: 사용자 식별 및 중복 방지
- `bookmarks.user_id`, `bookmarks.job_posting_id`: 사용자별 북마크 조회
- `applications.user_id`, `applications.job_posting_id`: 사용자별 지원현황 조회

## 확장 계획

- AI 분석 결과를 별도 테이블로 저장해 재사용
- 크롤링 원본 payload 저장 테이블 추가
- 크롤링 실행 로그와 실패 이력 저장
- 사용자별 추천 결과와 피드백 데이터 저장
