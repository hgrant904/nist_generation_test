"""Option model - represents response options for questions."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    question: Mapped["Question"] = relationship("Question", back_populates="options")

    def __repr__(self) -> str:
        return f"<Option(id={self.id}, text='{self.option_text[:50]}...')>"
