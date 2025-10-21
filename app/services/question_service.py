from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from app.models import Question
from app.schemas.question import QuestionCreate, QuestionUpdate

class QuestionService:
    @staticmethod
    def create_question(db: Session, question_data: QuestionCreate) -> Question:
        db_question = Question(**question_data.model_dump())
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    @staticmethod
    def get_question(db: Session, question_id: int) -> Optional[Question]:
        return db.query(Question).filter(Question.id == question_id).first()

    @staticmethod
    def get_questions_by_questionnaire(
        db: Session,
        questionnaire_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Question], int]:
        query = db.query(Question).filter(Question.questionnaire_id == questionnaire_id)
        total = query.count()
        questions = query.order_by(Question.order_index).offset(skip).limit(limit).all()
        return questions, total

    @staticmethod
    def update_question(
        db: Session,
        question_id: int,
        question_data: QuestionUpdate
    ) -> Optional[Question]:
        db_question = QuestionService.get_question(db, question_id)
        if not db_question:
            return None
        
        update_data = question_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_question, field, value)
        
        db.commit()
        db.refresh(db_question)
        return db_question

    @staticmethod
    def delete_question(db: Session, question_id: int) -> bool:
        db_question = QuestionService.get_question(db, question_id)
        if not db_question:
            return False
        
        db.delete(db_question)
        db.commit()
        return True

    @staticmethod
    def validate_dependencies(db: Session, question: Question, answered_questions: dict) -> bool:
        if not question.depends_on_question_id:
            return True
        
        dependency_answer = answered_questions.get(question.depends_on_question_id)
        if not dependency_answer:
            return False
        
        if question.depends_on_answer:
            return dependency_answer == question.depends_on_answer
        
        return True
