# ERD 설계 개요

## 1. 핵심 엔티티
- Company: 기업 정보
- JobPosting: 채용 공고
- Skill: 기술 스택
- JobSkill: 공고와 기술 스택의 다대다 연결 테이블
- User: 사용자
- Bookmark: 사용자의 공고 북마크
- Application: 사용자의 지원 내역
- Resume: 사용자 이력서
- ResumeAnalysis: 이력서 분석 결과
- CompanyFollow: 사용자의 기업 팔로우
- Notification: 사용자 알림

## 2. 관계 요약
- Company 1:N JobPosting
- JobPosting N:M Skill (via JobSkill)
- User 1:N Bookmark
- User 1:N Application
- User 1:N Resume
- Resume 1:N ResumeAnalysis
- User 1:N CompanyFollow
- User 1:N Notification

## 3. 주요 제약조건
- 각 테이블은 created_at, updated_at 컬럼을 포함한다.
- 외래 키는 삭제 시 연관 데이터 정합성을 유지하기 위해 ondelete 옵션을 설정한다.
- 중복 북마크, 지원, 팔로우를 방지하기 위해 UniqueConstraint를 적용한다.

## 4. 권장 인덱스
- companies.name
- job_postings.company_id
- job_postings.title
- skills.name
- users.email
- bookmarks.user_id, bookmarks.job_posting_id
- applications.user_id, applications.job_posting_id
- resumes.user_id
- resume_analyses.resume_id, resume_analyses.job_posting_id
- company_follows.user_id, company_follows.company_id
- notifications.user_id, notifications.is_read
