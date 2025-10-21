"""Response model - represents user responses to assessment questions."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    option_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("options.id", ondelete="SET NULL"), nullable=True, index=True
    )
    text_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    numeric_response: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    response_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="responses")
    question: Mapped["Question"] = relationship("Question", back_populates="responses")
    option: Mapped[Optional["Option"]] = relationship("Option")
    evidences: Mapped[List["Evidence"]] = relationship(
        "Evidence", back_populates="response", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Response(id={self.id}, assessment_id={self.assessment_id}, question_id={self.question_id})>"
