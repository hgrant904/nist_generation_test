from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.nist import NistCategory, NistFunction, NistQuestion, NistSubcategory
from app.schemas import (
    NistCategorySchema,
    NistFunctionSchema,
    NistQuestionSchema,
    NistSubcategorySchema,
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=list[NistQuestionSchema])
async def list_questions(session: AsyncSession = Depends(get_db)) -> list[NistQuestionSchema]:
    result = await session.execute(
        select(NistQuestion).order_by(NistQuestion.order_index, NistQuestion.code)
    )
    questions = result.scalars().all()
    return [NistQuestionSchema.model_validate(question) for question in questions]


@router.get("/functions", response_model=list[NistFunctionSchema])
async def list_functions(session: AsyncSession = Depends(get_db)) -> list[NistFunctionSchema]:
    result = await session.execute(select(NistFunction).order_by(NistFunction.code))
    functions = result.scalars().all()
    return [NistFunctionSchema.model_validate(function) for function in functions]


@router.get("/categories", response_model=list[NistCategorySchema])
async def list_categories(session: AsyncSession = Depends(get_db)) -> list[NistCategorySchema]:
    result = await session.execute(select(NistCategory).order_by(NistCategory.code))
    categories = result.scalars().all()
    return [NistCategorySchema.model_validate(category) for category in categories]


@router.get("/subcategories", response_model=list[NistSubcategorySchema])
async def list_subcategories(
    session: AsyncSession = Depends(get_db),
) -> list[NistSubcategorySchema]:
    result = await session.execute(select(NistSubcategory).order_by(NistSubcategory.code))
    subcategories = result.scalars().all()
    return [NistSubcategorySchema.model_validate(subcategory) for subcategory in subcategories]
