from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class NistQuestionSchema(BaseModel):
    id: UUID
    code: str
    prompt: str
    guidance: str | None = None
    answer_type: str
    order_index: int

    model_config = {"from_attributes": True}


class NistSubcategorySchema(BaseModel):
    id: UUID
    code: str
    description: str

    model_config = {"from_attributes": True}


class NistCategorySchema(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class NistFunctionSchema(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}
