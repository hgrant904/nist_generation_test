from .questionnaires import router as questionnaires_router
from .questions import router as questions_router
from .assessments import router as assessments_router

__all__ = ["questionnaires_router", "questions_router", "assessments_router"]
