from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from app.models import Questionnaire
from app.schemas.questionnaire import QuestionnaireCreate, QuestionnaireUpdate

class QuestionnaireService:
    @staticmethod
    def create_questionnaire(db: Session, questionnaire_data: QuestionnaireCreate) -> Questionnaire:
        db_questionnaire = Questionnaire(**questionnaire_data.model_dump())
        db.add(db_questionnaire)
        db.commit()
        db.refresh(db_questionnaire)
        return db_questionnaire

    @staticmethod
    def get_questionnaire(db: Session, questionnaire_id: int) -> Optional[Questionnaire]:
        return db.query(Questionnaire).filter(Questionnaire.id == questionnaire_id).first()

    @staticmethod
    def get_questionnaires(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Questionnaire], int]:
        query = db.query(Questionnaire)
        
        if category:
            query = query.filter(Questionnaire.category == category)
        if is_active is not None:
            query = query.filter(Questionnaire.is_active == is_active)
        
        total = query.count()
        questionnaires = query.offset(skip).limit(limit).all()
        
        return questionnaires, total

    @staticmethod
    def update_questionnaire(
        db: Session,
        questionnaire_id: int,
        questionnaire_data: QuestionnaireUpdate
    ) -> Optional[Questionnaire]:
        db_questionnaire = QuestionnaireService.get_questionnaire(db, questionnaire_id)
        if not db_questionnaire:
            return None
        
        update_data = questionnaire_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_questionnaire, field, value)
        
        db.commit()
        db.refresh(db_questionnaire)
        return db_questionnaire

    @staticmethod
    def delete_questionnaire(db: Session, questionnaire_id: int) -> bool:
        db_questionnaire = QuestionnaireService.get_questionnaire(db, questionnaire_id)
        if not db_questionnaire:
            return False
        
        db.delete(db_questionnaire)
        db.commit()
        return True
