from __future__ import annotations

from typing import Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import Assessment, AssessmentResponse, AssessmentStatus
from app.models.nist import NistQuestion


async def ensure_assessment_exists(session: AsyncSession, assessment_id: UUID) -> Assessment:
    result = await session.execute(select(Assessment).where(Assessment.id == assessment_id))
    assessment = result.scalar_one_or_none()
    if assessment is None:
        raise NoResultFound(f"Assessment {assessment_id} not found")
    return assessment


async def fetch_first_question(session: AsyncSession) -> NistQuestion | None:
    stmt = select(NistQuestion).order_by(NistQuestion.order_index, NistQuestion.code)
    result = await session.execute(stmt)
    return result.scalars().first()


async def fetch_next_question(
    session: AsyncSession, assessment_id: UUID
) -> Tuple[NistQuestion | None, int]:
    answered_rows = await session.execute(
        select(AssessmentResponse.question_id).where(AssessmentResponse.assessment_id == assessment_id)
    )
    answered_ids = {row[0] for row in answered_rows.all()}

    stmt = select(NistQuestion).order_by(NistQuestion.order_index, NistQuestion.code)
    result = await session.execute(stmt)
    questions = result.scalars().all()

    unanswered_questions = [question for question in questions if question.id not in answered_ids]

    if not unanswered_questions:
        assessment = await ensure_assessment_exists(session, assessment_id)
        if assessment.status != AssessmentStatus.COMPLETED.value:
            assessment.status = AssessmentStatus.COMPLETED.value
            await session.commit()
            await session.refresh(assessment)
        return None, 0

    next_question = unanswered_questions[0]
    remaining_after_answer = max(len(unanswered_questions) - 1, 0)
    return next_question, remaining_after_answer


async def record_response(
    session: AsyncSession,
    assessment_id: UUID,
    question_id: UUID,
    answer: str,
    notes: str | None = None,
) -> AssessmentResponse:
    assessment = await ensure_assessment_exists(session, assessment_id)

    result = await session.execute(
        select(AssessmentResponse).where(
            AssessmentResponse.assessment_id == assessment_id,
            AssessmentResponse.question_id == question_id,
        )
    )
    response = result.scalar_one_or_none()

    if response is None:
        response = AssessmentResponse(
            assessment_id=assessment_id,
            question_id=question_id,
            answer=answer,
            notes=notes,
        )
        session.add(response)
    else:
        response.answer = answer
        response.notes = notes

    await session.commit()
    await session.refresh(response)

    await _refresh_assessment_status(session, assessment)
    return response


async def calculate_progress(session: AsyncSession, assessment_id: UUID) -> dict[str, int | float | str]:
    assessment = await ensure_assessment_exists(session, assessment_id)

    total = await session.scalar(select(func.count()).select_from(NistQuestion))
    answered = await session.scalar(
        select(func.count())
        .select_from(AssessmentResponse)
        .where(AssessmentResponse.assessment_id == assessment_id)
    )

    total_questions = int(total or 0)
    answered_questions = int(answered or 0)
    completion_percentage = (
        (answered_questions / total_questions) * 100 if total_questions > 0 else 0.0
    )

    return {
        "assessment_id": assessment_id,
        "answered_questions": answered_questions,
        "total_questions": total_questions,
        "completion_percentage": round(completion_percentage, 2),
        "status": assessment.status,
    }


async def _refresh_assessment_status(session: AsyncSession, assessment: Assessment) -> None:
    total = await session.scalar(select(func.count()).select_from(NistQuestion))
    answered = await session.scalar(
        select(func.count())
        .select_from(AssessmentResponse)
        .where(AssessmentResponse.assessment_id == assessment.id)
    )

    total_questions = int(total or 0)
    answered_questions = int(answered or 0)

    if total_questions and answered_questions >= total_questions:
        new_status = AssessmentStatus.COMPLETED.value
    else:
        new_status = AssessmentStatus.IN_PROGRESS.value

    if assessment.status != new_status:
        assessment.status = new_status
        await session.commit()
        await session.refresh(assessment)
