from fastapi import APIRouter

from app.api.routes import assessments, chat, health, questions

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(assessments.router)
api_router.include_router(questions.router)
api_router.include_router(chat.router)

__all__ = ["api_router"]
