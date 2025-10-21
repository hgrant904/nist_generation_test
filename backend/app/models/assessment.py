from __future__ import annotations

import enum
import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.nist import NistQuestion


class AssessmentStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Assessment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assessments"

    name: Mapped[str | None] = mapped_column(String(150), default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(
        String(20), default=AssessmentStatus.IN_PROGRESS.value, nullable=False
    )

    responses: Mapped[list["AssessmentResponse"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )


class AssessmentResponse(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assessment_responses"
    __table_args__ = (
        UniqueConstraint("assessment_id", "question_id", name="uq_assessment_question"),
    )

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nist_questions.id", ondelete="CASCADE"), nullable=False
    )
    answer: Mapped[str | None] = mapped_column(Text, default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)

    assessment: Mapped[Assessment] = relationship(back_populates="responses")
    question: Mapped[NistQuestion] = relationship()
