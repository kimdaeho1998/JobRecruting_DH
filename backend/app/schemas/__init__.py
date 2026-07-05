from datetime import datetime
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
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    description: Optional[str] = None
    salary_range: Optional[str] = None
    source_url: Optional[str] = None
    is_active: bool = True


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingRead(JobPostingBase, TimestampSchema):
    id: int


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
    pass


class BookmarkRead(BookmarkBase, TimestampSchema):
    id: int
    user_id: int


class ApplicationBase(BaseModel):
    job_posting_id: int
    status: str = "saved"
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationRead(ApplicationBase, TimestampSchema):
    id: int
    user_id: int
    applied_at: Optional[datetime] = None


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
    pass


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
