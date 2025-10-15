from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class SessionStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    user_id = Column(String(255))
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.IN_PROGRESS)
    current_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    questionnaire = relationship("Questionnaire", back_populates="assessment_sessions")
    responses = relationship("Response", back_populates="session", cascade="all, delete-orphan")
