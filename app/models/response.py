from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_value = Column(Text, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("AssessmentSession", back_populates="responses")
    question = relationship("Question", back_populates="responses")

    __table_args__ = (
        UniqueConstraint('session_id', 'question_id', name='unique_session_question'),
    )
