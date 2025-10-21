"""Assessment model - represents an assessment instance."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from ..database import Base


class AssessmentStatus(enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    framework: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    framework_version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[AssessmentStatus] = mapped_column(
        SQLEnum(AssessmentStatus, name="assessment_status_enum"),
        default=AssessmentStatus.DRAFT,
        nullable=False,
        index=True,
    )
    organization_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    assessor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    sessions: Mapped[List["AssessmentSession"]] = relationship(
        "AssessmentSession", back_populates="assessment", cascade="all, delete-orphan"
    )
    responses: Mapped[List["Response"]] = relationship(
        "Response", back_populates="assessment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Assessment(id={self.id}, name='{self.name}', status='{self.status.value}')>"
