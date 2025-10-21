from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)
    order_index = Column(Integer, default=0)
    is_required = Column(Boolean, default=True)
    options = Column(JSON)
    branching_rules = Column(JSON)
    depends_on_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    depends_on_answer = Column(String(255), nullable=True)
    question_metadata = Column(JSON)

    questionnaire = relationship("Questionnaire", back_populates="questions")
    responses = relationship("Response", back_populates="question")
    dependent_questions = relationship("Question", remote_side=[depends_on_question_id])
