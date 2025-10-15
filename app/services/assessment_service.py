from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
import uuid
from app.models import AssessmentSession, Response, Question
from app.models.assessment_session import SessionStatus
from app.schemas.assessment import AssessmentSessionCreate, ResponseSubmit
from app.services.question_service import QuestionService

class AssessmentService:
    @staticmethod
    def start_assessment(db: Session, session_data: AssessmentSessionCreate) -> AssessmentSession:
        session_token = str(uuid.uuid4())
        
        db_session = AssessmentSession(
            questionnaire_id=session_data.questionnaire_id,
            user_id=session_data.user_id,
            session_token=session_token,
            status=SessionStatus.IN_PROGRESS
        )
        
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        
        return db_session

    @staticmethod
    def get_session(db: Session, session_token: str) -> Optional[AssessmentSession]:
        return db.query(AssessmentSession).filter(
            AssessmentSession.session_token == session_token
        ).first()

    @staticmethod
    def get_session_by_id(db: Session, session_id: int) -> Optional[AssessmentSession]:
        return db.query(AssessmentSession).filter(
            AssessmentSession.id == session_id
        ).first()

    @staticmethod
    def get_answered_questions(db: Session, session_id: int) -> dict:
        responses = db.query(Response).filter(Response.session_id == session_id).all()
        return {response.question_id: response.answer_value for response in responses}

    @staticmethod
    def resolve_next_question(db: Session, session: AssessmentSession) -> Optional[Question]:
        answered_questions = AssessmentService.get_answered_questions(db, session.id)
        
        all_questions = db.query(Question).filter(
            Question.questionnaire_id == session.questionnaire_id
        ).order_by(Question.order_index).all()
        
        for question in all_questions:
            if question.id in answered_questions:
                continue
            
            if QuestionService.validate_dependencies(db, question, answered_questions):
                if question.id in answered_questions:
                    last_response = db.query(Response).filter(
                        Response.session_id == session.id,
                        Response.question_id == question.id
                    ).first()
                    
                    if last_response and question.branching_rules:
                        next_question_id = AssessmentService.evaluate_branching_rules(
                            question.branching_rules,
                            last_response.answer_value
                        )
                        if next_question_id:
                            next_question = QuestionService.get_question(db, next_question_id)
                            if next_question and next_question.id not in answered_questions:
                                return next_question
                    continue
                
                return question
        
        return None

    @staticmethod
    def evaluate_branching_rules(branching_rules: List[dict], answer_value: str) -> Optional[int]:
        for rule in branching_rules:
            condition = rule.get("condition")
            next_question_id = rule.get("next_question_id")
            
            if condition == "equals" and rule.get("value") == answer_value:
                return next_question_id
            elif condition == "not_equals" and rule.get("value") != answer_value:
                return next_question_id
            elif condition == "contains" and rule.get("value") in answer_value:
                return next_question_id
        
        return None

    @staticmethod
    def submit_response(db: Session, response_data: ResponseSubmit) -> Response:
        session = AssessmentService.get_session(db, response_data.session_token)
        if not session:
            raise ValueError("Invalid session token")
        
        if session.status != SessionStatus.IN_PROGRESS:
            raise ValueError("Session is not active")
        
        question = QuestionService.get_question(db, response_data.question_id)
        if not question:
            raise ValueError("Invalid question ID")
        
        if question.questionnaire_id != session.questionnaire_id:
            raise ValueError("Question does not belong to this questionnaire")
        
        answered_questions = AssessmentService.get_answered_questions(db, session.id)
        if not QuestionService.validate_dependencies(db, question, answered_questions):
            raise ValueError("Question dependencies not met")
        
        existing_response = db.query(Response).filter(
            Response.session_id == session.id,
            Response.question_id == response_data.question_id
        ).first()
        
        if existing_response:
            existing_response.answer_value = response_data.answer_value
            existing_response.answered_at = datetime.now(timezone.utc)
            db_response = existing_response
        else:
            db_response = Response(
                session_id=session.id,
                question_id=response_data.question_id,
                answer_value=response_data.answer_value
            )
            db.add(db_response)
        
        session.current_question_id = response_data.question_id
        session.last_activity_at = datetime.now(timezone.utc)
        
        db.flush()
        
        next_question = AssessmentService.resolve_next_question(db, session)
        if not next_question:
            session.status = SessionStatus.COMPLETED
            session.completed_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(db_response)
        
        return db_response

    @staticmethod
    def get_session_responses(db: Session, session_id: int) -> List[Response]:
        return db.query(Response).filter(Response.session_id == session_id).all()
