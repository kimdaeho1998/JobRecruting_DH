from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    ApplicationCreate,
    ApplicationListItem,
    ApplicationRead,
    ApplicationUpdate,
    BookmarkCreate,
    BookmarkRead,
    CompanyFollowCreate,
    CompanyFollowRead,
    CompanyRead,
    DashboardStats,
    JobPostingDetail,
    JobPostingSummary,
    SkillRead,
)
from app.schemas import AIAnalysisRequest, AIAnalysisResponse
from app.services.ai_service import AIService
from app.services.application_service import ApplicationService
from app.services.bookmark_service import BookmarkService
from app.services.catalog_service import CatalogService
from app.services.company_follow_service import CompanyFollowService
from app.services.dashboard_service import DashboardService
from app.services.job_posting_service import JobPostingService

router = APIRouter()


@router.get("/job-postings", response_model=list[JobPostingSummary], tags=["job-postings"])
def list_job_postings(
    q: Optional[str] = Query(default=None, description="제목, 설명, 회사명 통합 검색어"),
    job_category: Optional[str] = Query(default=None, description="직무 필터"),
    company_name: Optional[str] = Query(default=None, description="회사명 필터"),
    location: Optional[str] = Query(default=None, description="지역 필터"),
    experience_level: Optional[str] = Query(default=None, description="경력 필터"),
    skill: Optional[str] = Query(default=None, description="기술스택 필터"),
    deadline_from: Optional[date] = Query(default=None, description="마감일 시작"),
    deadline_to: Optional[date] = Query(default=None, description="마감일 종료"),
    is_active: Optional[bool] = Query(default=True, description="활성 공고 여부"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = JobPostingService(db)
    return service.list_job_postings(
        q=q,
        job_category=job_category,
        company_name=company_name,
        location=location,
        experience_level=experience_level,
        skill=skill,
        deadline_from=deadline_from,
        deadline_to=deadline_to,
        is_active=is_active,
        offset=offset,
        limit=limit,
    )


@router.get("/job-postings/search", response_model=list[JobPostingSummary], tags=["job-postings"])
def search_job_postings(
    q: str = Query(..., min_length=1, description="검색어"),
    job_category: Optional[str] = Query(default=None),
    company_name: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    experience_level: Optional[str] = Query(default=None),
    skill: Optional[str] = Query(default=None),
    deadline_from: Optional[date] = Query(default=None),
    deadline_to: Optional[date] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = JobPostingService(db)
    return service.list_job_postings(
        q=q,
        job_category=job_category,
        company_name=company_name,
        location=location,
        experience_level=experience_level,
        skill=skill,
        deadline_from=deadline_from,
        deadline_to=deadline_to,
        offset=offset,
        limit=limit,
    )


@router.get("/job-postings/{job_posting_id}", response_model=JobPostingDetail, tags=["job-postings"])
def get_job_posting(job_posting_id: int, db: Session = Depends(get_db)):
    service = JobPostingService(db)
    posting = service.get_job_posting(job_posting_id)
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")
    return posting


@router.get("/companies", response_model=list[CompanyRead], tags=["catalog"])
def list_companies(
    name: Optional[str] = Query(default=None, description="회사명 검색어"),
    db: Session = Depends(get_db),
):
    return CatalogService(db).list_companies(name)


@router.get("/skills", response_model=list[SkillRead], tags=["catalog"])
def list_skills(
    name: Optional[str] = Query(default=None, description="기술명 검색어"),
    db: Session = Depends(get_db),
):
    return CatalogService(db).list_skills(name)


@router.post("/bookmarks", response_model=BookmarkRead, status_code=status.HTTP_201_CREATED, tags=["bookmarks"])
def add_bookmark(payload: BookmarkCreate, db: Session = Depends(get_db)):
    return BookmarkService(db).add_bookmark(payload.user_id, payload.job_posting_id)


@router.delete("/bookmarks", status_code=status.HTTP_204_NO_CONTENT, tags=["bookmarks"])
def delete_bookmark(
    user_id: int = Query(default=1),
    job_posting_id: int = Query(...),
    db: Session = Depends(get_db),
):
    BookmarkService(db).delete_bookmark(user_id, job_posting_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/applications", response_model=list[ApplicationListItem], tags=["applications"])
def list_applications(
    user_id: int = Query(default=1),
    db: Session = Depends(get_db),
):
    return ApplicationService(db).list_applications(user_id)


@router.post(
    "/applications",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
    tags=["applications"],
)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    return ApplicationService(db).create_application(
        user_id=payload.user_id,
        job_posting_id=payload.job_posting_id,
        status_value=payload.status,
        notes=payload.notes,
        applied_at=payload.applied_at,
        deadline=payload.deadline,
    )


@router.patch("/applications/{application_id}", response_model=ApplicationRead, tags=["applications"])
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    return ApplicationService(db).update_application(application_id, payload)


@router.post(
    "/company-follows",
    response_model=CompanyFollowRead,
    status_code=status.HTTP_201_CREATED,
    tags=["company-follows"],
)
def add_company_follow(payload: CompanyFollowCreate, db: Session = Depends(get_db)):
    return CompanyFollowService(db).add_company_follow(payload.user_id, payload.company_id)


@router.delete("/company-follows", status_code=status.HTTP_204_NO_CONTENT, tags=["company-follows"])
def delete_company_follow(
    user_id: int = Query(default=1),
    company_id: int = Query(...),
    db: Session = Depends(get_db),
):
    CompanyFollowService(db).delete_company_follow(user_id, company_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/dashboard/stats", response_model=DashboardStats, tags=["dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    return DashboardService(db).get_stats()


@router.post("/ai/analyze", response_model=AIAnalysisResponse, tags=["ai"])
def analyze_with_ai(payload: AIAnalysisRequest):
    service = AIService()
    prompt_file = payload.prompt_file or "job_summary.prompt.md"
    result = service.generate_response(
        prompt_file,
        company_name=payload.company_name,
        job_title=payload.job_title,
        job_description=payload.job_description,
        resume_text=payload.resume_text,
        job_a_title=payload.job_a_title,
        job_a_description=payload.job_a_description,
        job_b_title=payload.job_b_title,
        job_b_description=payload.job_b_description,
    )
    return AIAnalysisResponse(prompt_file=prompt_file, result=result)


@router.post("/ai/summary", response_model=AIAnalysisResponse, tags=["ai"])
def generate_job_summary(payload: AIAnalysisRequest):
    return _analyze_with_prompt("job_summary.prompt.md", payload)


@router.post("/ai/skills", response_model=AIAnalysisResponse, tags=["ai"])
def extract_job_skills(payload: AIAnalysisRequest):
    return _analyze_with_prompt("skill_extraction.prompt.md", payload)


@router.post("/ai/fit", response_model=AIAnalysisResponse, tags=["ai"])
def analyze_job_fit(payload: AIAnalysisRequest):
    return _analyze_with_prompt("job_fit_analysis.prompt.md", payload)


@router.post("/ai/resume", response_model=AIAnalysisResponse, tags=["ai"])
def analyze_resume(payload: AIAnalysisRequest):
    return _analyze_with_prompt("resume_analysis.prompt.md", payload)


@router.post("/ai/cover-letter", response_model=AIAnalysisResponse, tags=["ai"])
def generate_cover_letter(payload: AIAnalysisRequest):
    return _analyze_with_prompt("cover_letter.prompt.md", payload)


@router.post("/ai/interview-questions", response_model=AIAnalysisResponse, tags=["ai"])
def generate_interview_questions(payload: AIAnalysisRequest):
    return _analyze_with_prompt("interview_questions.prompt.md", payload)


@router.post("/ai/company-analysis", response_model=AIAnalysisResponse, tags=["ai"])
def analyze_company(payload: AIAnalysisRequest):
    return _analyze_with_prompt("company_analysis.prompt.md", payload)


@router.post("/ai/compare", response_model=AIAnalysisResponse, tags=["ai"])
def compare_jobs(payload: AIAnalysisRequest):
    return _analyze_with_prompt("job_compare.prompt.md", payload)


def _analyze_with_prompt(prompt_file: str, payload: AIAnalysisRequest) -> AIAnalysisResponse:
    service = AIService()
    result = service.generate_response(
        prompt_file,
        company_name=payload.company_name,
        job_title=payload.job_title,
        job_description=payload.job_description,
        resume_text=payload.resume_text,
        job_a_title=payload.job_a_title,
        job_a_description=payload.job_a_description,
        job_b_title=payload.job_b_title,
        job_b_description=payload.job_b_description,
    )
    return AIAnalysisResponse(prompt_file=prompt_file, result=result)
