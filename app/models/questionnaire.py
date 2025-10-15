from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    version = Column(String(50), default="1.0")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    questions = relationship("Question", back_populates="questionnaire", cascade="all, delete-orphan")
    assessment_sessions = relationship("AssessmentSession", back_populates="questionnaire")
