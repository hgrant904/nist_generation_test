from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.nist import NistQuestionSchema


class AssessmentCreateRequest(BaseModel):
    name: str | None = Field(default=None, description="Optional display name for the assessment")
    description: str | None = Field(default=None, description="Assessment description")


class AssessmentCreateResponse(BaseModel):
    assessment_id: UUID
    status: str
    first_question: NistQuestionSchema | None = None


class AssessmentQuestionResponse(BaseModel):
    question: NistQuestionSchema | None = None
    remaining_questions: int


class AssessmentResponsePayload(BaseModel):
    question_id: UUID
    answer: str
    notes: str | None = None


class AssessmentResponseSchema(BaseModel):
    id: UUID
    assessment_id: UUID
    question_id: UUID
    answer: str | None
    notes: str | None

    model_config = {"from_attributes": True}


class AssessmentProgressSchema(BaseModel):
    assessment_id: UUID
    answered_questions: int
    total_questions: int
    completion_percentage: float
    status: str
