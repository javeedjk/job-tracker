from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import ApplicationStatus, ResearchStatus


# ---------- USER SCHEMAS ----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # plain text input, will be hashed before saving


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # allows reading directly from SQLAlchemy model objects


# --------- APPLICATION SCHEMAS ---------

class ApplicationCreate(BaseModel):
    company_name: str
    role_title: str
    status: Optional[ApplicationStatus] = ApplicationStatus.APPLIED
    date_applied: Optional[datetime] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    role_title: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    date_applied: Optional[datetime] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    company_name: str
    role_title: str
    status: ApplicationStatus
    date_applied: Optional[datetime]
    job_url: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --------- RESEARCH AGENT SCHEMAS ---------

class ResearchStatusOut(BaseModel):
    research_status: ResearchStatus
    research_report: Optional[str] = None
    research_generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True