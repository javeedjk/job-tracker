import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base


class ApplicationStatus(str, enum.Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class ResearchStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="owner")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    company_name = Column(String, nullable=False)
    role_title = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)
    date_applied = Column(DateTime, default=datetime.utcnow)
    job_url = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # --- new: company research agent fields ---
    research_report = Column(Text, nullable=True)
    research_status = Column(Enum(ResearchStatus), default=ResearchStatus.NOT_STARTED, nullable=False)
    research_generated_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="applications")