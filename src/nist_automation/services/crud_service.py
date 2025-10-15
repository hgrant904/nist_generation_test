"""CRUD service layer for core entities."""

from typing import Optional, List, Dict, Any, Type
from sqlalchemy.orm import Session
from ..repositories.base import BaseRepository
from ..models import (
    ControlFamily,
    Control,
    ImplementationTier,
    Question,
    Option,
    Assessment,
    AssessmentSession,
    Response,
    Evidence,
)


class CRUDService:

    def __init__(self, db: Session):
        self.db = db
        self.control_family_repo = BaseRepository(ControlFamily, db)
        self.control_repo = BaseRepository(Control, db)
        self.implementation_tier_repo = BaseRepository(ImplementationTier, db)
        self.question_repo = BaseRepository(Question, db)
        self.option_repo = BaseRepository(Option, db)
        self.assessment_repo = BaseRepository(Assessment, db)
        self.session_repo = BaseRepository(AssessmentSession, db)
        self.response_repo = BaseRepository(Response, db)
        self.evidence_repo = BaseRepository(Evidence, db)

    def create_control_family(self, **kwargs: Any) -> ControlFamily:
        return self.control_family_repo.create(**kwargs)

    def get_control_family(self, id: int) -> Optional[ControlFamily]:
        return self.control_family_repo.get_by_id(id)

    def get_control_families(
        self, framework: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[ControlFamily]:
        if framework:
            return self.control_family_repo.get_by_filters({"framework": framework}, skip, limit)
        return self.control_family_repo.get_all(skip, limit)

    def update_control_family(self, id: int, **kwargs: Any) -> Optional[ControlFamily]:
        return self.control_family_repo.update(id, **kwargs)

    def delete_control_family(self, id: int) -> bool:
        return self.control_family_repo.delete(id)

    def create_control(self, **kwargs: Any) -> Control:
        return self.control_repo.create(**kwargs)

    def get_control(self, id: int) -> Optional[Control]:
        return self.control_repo.get_by_id(id)

    def get_controls(
        self, family_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Control]:
        if family_id:
            return self.control_repo.get_by_filters({"family_id": family_id}, skip, limit)
        return self.control_repo.get_all(skip, limit)

    def update_control(self, id: int, **kwargs: Any) -> Optional[Control]:
        return self.control_repo.update(id, **kwargs)

    def delete_control(self, id: int) -> bool:
        return self.control_repo.delete(id)

    def create_implementation_tier(self, **kwargs: Any) -> ImplementationTier:
        return self.implementation_tier_repo.create(**kwargs)

    def get_implementation_tier(self, id: int) -> Optional[ImplementationTier]:
        return self.implementation_tier_repo.get_by_id(id)

    def get_implementation_tiers(self, skip: int = 0, limit: int = 100) -> List[ImplementationTier]:
        return self.implementation_tier_repo.get_all(skip, limit)

    def create_question(self, **kwargs: Any) -> Question:
        return self.question_repo.create(**kwargs)

    def get_question(self, id: int) -> Optional[Question]:
        return self.question_repo.get_by_id(id)

    def get_questions(
        self, control_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Question]:
        if control_id:
            return self.question_repo.get_by_filters({"control_id": control_id}, skip, limit)
        return self.question_repo.get_all(skip, limit)

    def update_question(self, id: int, **kwargs: Any) -> Optional[Question]:
        return self.question_repo.update(id, **kwargs)

    def delete_question(self, id: int) -> bool:
        return self.question_repo.delete(id)

    def create_option(self, **kwargs: Any) -> Option:
        return self.option_repo.create(**kwargs)

    def get_option(self, id: int) -> Optional[Option]:
        return self.option_repo.get_by_id(id)

    def get_options(
        self, question_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Option]:
        if question_id:
            return self.option_repo.get_by_filters({"question_id": question_id}, skip, limit)
        return self.option_repo.get_all(skip, limit)

    def create_assessment(self, **kwargs: Any) -> Assessment:
        return self.assessment_repo.create(**kwargs)

    def get_assessment(self, id: int) -> Optional[Assessment]:
        return self.assessment_repo.get_by_id(id)

    def get_assessments(self, skip: int = 0, limit: int = 100) -> List[Assessment]:
        return self.assessment_repo.get_all(skip, limit)

    def update_assessment(self, id: int, **kwargs: Any) -> Optional[Assessment]:
        return self.assessment_repo.update(id, **kwargs)

    def delete_assessment(self, id: int) -> bool:
        return self.assessment_repo.delete(id)

    def create_assessment_session(self, **kwargs: Any) -> AssessmentSession:
        return self.session_repo.create(**kwargs)

    def get_assessment_session(self, id: int) -> Optional[AssessmentSession]:
        return self.session_repo.get_by_id(id)

    def create_response(self, **kwargs: Any) -> Response:
        return self.response_repo.create(**kwargs)

    def get_response(self, id: int) -> Optional[Response]:
        return self.response_repo.get_by_id(id)

    def get_responses(
        self, assessment_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Response]:
        if assessment_id:
            return self.response_repo.get_by_filters({"assessment_id": assessment_id}, skip, limit)
        return self.response_repo.get_all(skip, limit)

    def update_response(self, id: int, **kwargs: Any) -> Optional[Response]:
        return self.response_repo.update(id, **kwargs)

    def create_evidence(self, **kwargs: Any) -> Evidence:
        return self.evidence_repo.create(**kwargs)

    def get_evidence(self, id: int) -> Optional[Evidence]:
        return self.evidence_repo.get_by_id(id)

    def get_evidences(
        self, response_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Evidence]:
        if response_id:
            return self.evidence_repo.get_by_filters({"response_id": response_id}, skip, limit)
        return self.evidence_repo.get_all(skip, limit)
