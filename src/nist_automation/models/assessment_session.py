"""Assessment Session model - represents user sessions conducting assessments."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    user_identifier: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    last_activity: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<AssessmentSession(id={self.id}, assessment_id={self.assessment_id})>"
