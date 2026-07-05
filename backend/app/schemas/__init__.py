from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TimestampSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase, TimestampSchema):
    id: int


class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillRead(SkillBase, TimestampSchema):
    id: int


class JobPostingBase(BaseModel):
    company_id: int
    title: str = Field(..., min_length=1, max_length=255)
    job_category: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    description: Optional[str] = None
    salary_range: Optional[str] = None
    deadline: Optional[date] = None
    source_site: Optional[str] = None
    source_url: Optional[str] = None
    is_active: bool = True


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingRead(JobPostingBase, TimestampSchema):
    id: int


class JobPostingSummary(BaseModel):
    id: int
    company_id: int
    company_name: str
    title: str
    job_category: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    deadline: Optional[date] = None
    source_site: Optional[str] = None
    source_url: Optional[str] = None
    is_active: bool
    skills: list[str] = []


class JobPostingDetail(JobPostingSummary):
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class JobPostingQuery(BaseModel):
    q: Optional[str] = None
    job_category: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None
    skill: Optional[str] = None
    deadline_from: Optional[date] = None
    deadline_to: Optional[date] = None
    is_active: Optional[bool] = True
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class JobSkillBase(BaseModel):
    job_posting_id: int
    skill_id: int


class JobSkillCreate(JobSkillBase):
    pass


class JobSkillRead(JobSkillBase, TimestampSchema):
    id: int


class UserBase(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase, TimestampSchema):
    id: int
    is_active: bool


class BookmarkBase(BaseModel):
    job_posting_id: int


class BookmarkCreate(BookmarkBase):
    user_id: int = 1


class BookmarkRead(BookmarkBase, TimestampSchema):
    id: int
    user_id: int


class ApplicationBase(BaseModel):
    job_posting_id: int
    status: str = "saved"
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    user_id: int = 1


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    applied_at: Optional[datetime] = None


class ApplicationRead(ApplicationBase, TimestampSchema):
    id: int
    user_id: int
    applied_at: Optional[datetime] = None


class ApplicationListItem(ApplicationRead):
    job_title: Optional[str] = None
    company_name: Optional[str] = None


class ResumeBase(BaseModel):
    title: Optional[str] = None
    content: str
    file_name: Optional[str] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeRead(ResumeBase, TimestampSchema):
    id: int
    user_id: int


class ResumeAnalysisBase(BaseModel):
    resume_id: int
    job_posting_id: Optional[int] = None
    score: Optional[int] = None
    summary: Optional[str] = None
    recommendations: Optional[str] = None


class ResumeAnalysisCreate(ResumeAnalysisBase):
    pass


class ResumeAnalysisRead(ResumeAnalysisBase, TimestampSchema):
    id: int


class CompanyFollowBase(BaseModel):
    company_id: int


class CompanyFollowCreate(CompanyFollowBase):
    user_id: int = 1


class CompanyFollowRead(CompanyFollowBase, TimestampSchema):
    id: int
    user_id: int


class NotificationBase(BaseModel):
    notification_type: str
    title: str
    body: Optional[str] = None
    is_read: bool = False
    related_type: Optional[str] = None
    related_id: Optional[int] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase, TimestampSchema):
    id: int
    user_id: int


class DashboardStats(BaseModel):
    total_job_postings: int
    active_job_postings: int
    total_companies: int
    total_skills: int
    total_bookmarks: int
    total_applications: int
    total_company_follows: int
    applications_by_status: dict[str, int]
