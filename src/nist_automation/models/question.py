"""Question model - represents assessment questions linked to controls."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, DateTime, Integer, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from ..database import Base


class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT = "text"
    RATING = "rating"
    YES_NO = "yes_no"
    FILE_UPLOAD = "file_upload"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    control_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(
        SQLEnum(QuestionType, name="question_type_enum"), nullable=False
    )
    help_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    control: Mapped["Control"] = relationship("Control", back_populates="questions")
    options: Mapped[List["Option"]] = relationship(
        "Option", back_populates="question", cascade="all, delete-orphan"
    )
    responses: Mapped[List["Response"]] = relationship(
        "Response", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, type='{self.question_type.value}')>"
