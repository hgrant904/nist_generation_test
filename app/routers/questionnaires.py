from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import math
from app.database import get_db
from app.services import QuestionnaireService
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireResponse,
    QuestionnaireList
)

router = APIRouter(
    prefix="/api/questionnaires",
    tags=["Questionnaires"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "/",
    response_model=QuestionnaireResponse,
    status_code=201,
    summary="Create a new questionnaire",
    description="Creates a new questionnaire with the provided details. The questionnaire will be used to organize questions for assessments."
)
def create_questionnaire(
    questionnaire: QuestionnaireCreate,
    db: Session = Depends(get_db)
):
    return QuestionnaireService.create_questionnaire(db, questionnaire)

@router.get(
    "/",
    response_model=QuestionnaireList,
    summary="List questionnaires",
    description="Retrieves a paginated list of questionnaires with optional filtering by category and active status."
)
def list_questionnaires(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    questionnaires, total = QuestionnaireService.get_questionnaires(
        db, skip=skip, limit=page_size, category=category, is_active=is_active
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return QuestionnaireList(
        items=questionnaires,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get(
    "/{questionnaire_id}",
    response_model=QuestionnaireResponse,
    summary="Get questionnaire by ID",
    description="Retrieves detailed information about a specific questionnaire."
)
def get_questionnaire(
    questionnaire_id: int,
    db: Session = Depends(get_db)
):
    questionnaire = QuestionnaireService.get_questionnaire(db, questionnaire_id)
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire

@router.patch(
    "/{questionnaire_id}",
    response_model=QuestionnaireResponse,
    summary="Update questionnaire",
    description="Updates an existing questionnaire with the provided fields."
)
def update_questionnaire(
    questionnaire_id: int,
    questionnaire: QuestionnaireUpdate,
    db: Session = Depends(get_db)
):
    updated = QuestionnaireService.update_questionnaire(db, questionnaire_id, questionnaire)
    if not updated:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return updated

@router.delete(
    "/{questionnaire_id}",
    status_code=204,
    summary="Delete questionnaire",
    description="Deletes a questionnaire and all associated questions and sessions."
)
def delete_questionnaire(
    questionnaire_id: int,
    db: Session = Depends(get_db)
):
    deleted = QuestionnaireService.delete_questionnaire(db, questionnaire_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return None
