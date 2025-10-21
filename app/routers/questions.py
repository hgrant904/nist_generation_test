from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import math
from app.database import get_db
from app.services import QuestionService
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse

router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=201,
    summary="Create a new question",
    description="Creates a new question within a questionnaire. Supports branching logic and dependency rules."
)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    return QuestionService.create_question(db, question)

@router.get(
    "/questionnaire/{questionnaire_id}",
    response_model=List[QuestionResponse],
    summary="List questions by questionnaire",
    description="Retrieves all questions for a specific questionnaire, ordered by order_index. Supports pagination."
)
def list_questions_by_questionnaire(
    questionnaire_id: int,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    db: Session = Depends(get_db)
):
    questions, total = QuestionService.get_questions_by_questionnaire(
        db, questionnaire_id, skip=skip, limit=limit
    )
    return questions

@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
    summary="Get question by ID",
    description="Retrieves detailed information about a specific question."
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    question = QuestionService.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.patch(
    "/{question_id}",
    response_model=QuestionResponse,
    summary="Update question",
    description="Updates an existing question with the provided fields."
)
def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db)
):
    updated = QuestionService.update_question(db, question_id, question)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated

@router.delete(
    "/{question_id}",
    status_code=204,
    summary="Delete question",
    description="Deletes a question from a questionnaire."
)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    deleted = QuestionService.delete_question(db, question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    return None
