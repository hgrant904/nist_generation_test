from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services import AssessmentService
from app.schemas.assessment import (
    AssessmentSessionCreate,
    AssessmentSessionResponse,
    QuestionResponse,
    ResponseSubmit,
    ResponseResponse
)

router = APIRouter(
    prefix="/api/assessments",
    tags=["Assessments"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/start",
    response_model=AssessmentSessionResponse,
    status_code=201,
    summary="Start a new assessment session",
    description="Creates a new assessment session for a questionnaire. Returns a session token to be used for submitting responses."
)
def start_assessment(
    session_data: AssessmentSessionCreate,
    db: Session = Depends(get_db)
):
    try:
        session = AssessmentService.start_assessment(db, session_data)
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/sessions/{session_token}",
    response_model=AssessmentSessionResponse,
    summary="Get assessment session",
    description="Retrieves the current state of an assessment session by its token."
)
def get_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    session = AssessmentService.get_session(db, session_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get(
    "/sessions/{session_token}/next-question",
    response_model=Optional[QuestionResponse],
    summary="Get next question",
    description="Resolves and returns the next question in the assessment based on branching logic and answered questions."
)
def get_next_question(
    session_token: str,
    db: Session = Depends(get_db)
):
    session = AssessmentService.get_session(db, session_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    next_question = AssessmentService.resolve_next_question(db, session)
    if not next_question:
        return None
    
    return QuestionResponse(
        id=next_question.id,
        question_text=next_question.question_text,
        question_type=next_question.question_type,
        is_required=next_question.is_required,
        options=next_question.options,
        question_metadata=next_question.question_metadata
    )

@router.post(
    "/responses",
    response_model=ResponseResponse,
    status_code=201,
    summary="Submit a response",
    description="Submits an answer to a question in an assessment session. Validates dependencies and updates session state."
)
def submit_response(
    response: ResponseSubmit,
    db: Session = Depends(get_db)
):
    try:
        db_response = AssessmentService.submit_response(db, response)
        return db_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/sessions/{session_token}/responses",
    response_model=List[ResponseResponse],
    summary="Get session responses",
    description="Retrieves all responses submitted in an assessment session."
)
def get_session_responses(
    session_token: str,
    db: Session = Depends(get_db)
):
    session = AssessmentService.get_session(db, session_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    responses = AssessmentService.get_session_responses(db, session.id)
    return responses

@router.post(
    "/sessions/{session_token}/resume",
    response_model=AssessmentSessionResponse,
    summary="Resume assessment session",
    description="Resumes a paused or in-progress assessment session, updating the last activity timestamp."
)
def resume_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    session = AssessmentService.get_session(db, session_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status.value == "completed":
        raise HTTPException(status_code=400, detail="Session is already completed")
    
    from datetime import datetime, timezone
    session.last_activity_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    
    return session
