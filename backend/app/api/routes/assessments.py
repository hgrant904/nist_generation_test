from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.assessment import Assessment, AssessmentResponse
from app.schemas import (
    AssessmentCreateRequest,
    AssessmentCreateResponse,
    AssessmentProgressSchema,
    AssessmentQuestionResponse,
    AssessmentResponsePayload,
    AssessmentResponseSchema,
    NistQuestionSchema,
)
from app.services.questionnaire import (
    calculate_progress,
    ensure_assessment_exists,
    fetch_first_question,
    fetch_next_question,
    record_response,
)

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("", response_model=AssessmentCreateResponse, status_code=status.HTTP_201_CREATED)
async def start_assessment(
    payload: AssessmentCreateRequest,
    session: AsyncSession = Depends(get_db),
) -> AssessmentCreateResponse:
    assessment = Assessment(name=payload.name, description=payload.description)
    session.add(assessment)
    await session.commit()
    await session.refresh(assessment)

    first_question = await fetch_first_question(session)

    first_question_schema = (
        NistQuestionSchema.model_validate(first_question) if first_question is not None else None
    )

    return AssessmentCreateResponse(
        assessment_id=assessment.id,
        status=assessment.status,
        first_question=first_question_schema,
    )


@router.get("/{assessment_id}", response_model=AssessmentProgressSchema)
async def get_assessment(
    assessment_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> AssessmentProgressSchema:
    try:
        progress = await calculate_progress(session, assessment_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return AssessmentProgressSchema(**progress)


@router.get(
    "/{assessment_id}/next-question",
    response_model=AssessmentQuestionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_next_question(
    assessment_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> AssessmentQuestionResponse:
    try:
        question, remaining = await fetch_next_question(session, assessment_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    question_schema = NistQuestionSchema.model_validate(question) if question else None

    return AssessmentQuestionResponse(
        question=question_schema,
        remaining_questions=remaining,
    )


@router.post(
    "/{assessment_id}/responses",
    response_model=AssessmentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def submit_response(
    assessment_id: UUID,
    payload: AssessmentResponsePayload,
    session: AsyncSession = Depends(get_db),
) -> AssessmentResponseSchema:
    try:
        response = await record_response(
            session,
            assessment_id=assessment_id,
            question_id=payload.question_id,
            answer=payload.answer,
            notes=payload.notes,
        )
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return AssessmentResponseSchema.model_validate(response)


@router.get(
    "/{assessment_id}/responses",
    response_model=list[AssessmentResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def list_responses(
    assessment_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> list[AssessmentResponseSchema]:
    try:
        await ensure_assessment_exists(session, assessment_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    result = await session.execute(
        select(AssessmentResponse)
        .where(AssessmentResponse.assessment_id == assessment_id)
        .order_by(AssessmentResponse.created_at)
    )
    responses = result.scalars().all()
    return [AssessmentResponseSchema.model_validate(resp) for resp in responses]


@router.get(
    "/{assessment_id}/progress",
    response_model=AssessmentProgressSchema,
    status_code=status.HTTP_200_OK,
)
async def get_progress(
    assessment_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> AssessmentProgressSchema:
    try:
        progress = await calculate_progress(session, assessment_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return AssessmentProgressSchema(**progress)
