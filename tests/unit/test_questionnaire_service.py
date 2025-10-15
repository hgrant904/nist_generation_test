import pytest
from app.services import QuestionnaireService
from app.schemas.questionnaire import QuestionnaireCreate, QuestionnaireUpdate

def test_create_questionnaire(db_session):
    questionnaire_data = QuestionnaireCreate(
        title="NIST 800-53 Assessment",
        description="Security controls assessment",
        category="security",
        version="1.0"
    )
    
    questionnaire = QuestionnaireService.create_questionnaire(db_session, questionnaire_data)
    
    assert questionnaire.id is not None
    assert questionnaire.title == "NIST 800-53 Assessment"
    assert questionnaire.category == "security"
    assert questionnaire.is_active is True

def test_get_questionnaire(db_session):
    questionnaire_data = QuestionnaireCreate(
        title="Test Questionnaire",
        description="Test description"
    )
    created = QuestionnaireService.create_questionnaire(db_session, questionnaire_data)
    
    retrieved = QuestionnaireService.get_questionnaire(db_session, created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.title == created.title

def test_get_questionnaire_not_found(db_session):
    retrieved = QuestionnaireService.get_questionnaire(db_session, 9999)
    assert retrieved is None

def test_get_questionnaires_with_pagination(db_session):
    for i in range(5):
        QuestionnaireService.create_questionnaire(
            db_session,
            QuestionnaireCreate(title=f"Questionnaire {i}", description=f"Desc {i}")
        )
    
    questionnaires, total = QuestionnaireService.get_questionnaires(db_session, skip=0, limit=3)
    
    assert len(questionnaires) == 3
    assert total == 5

def test_get_questionnaires_with_filter(db_session):
    QuestionnaireService.create_questionnaire(
        db_session,
        QuestionnaireCreate(title="Security Q", category="security")
    )
    QuestionnaireService.create_questionnaire(
        db_session,
        QuestionnaireCreate(title="Privacy Q", category="privacy")
    )
    
    questionnaires, total = QuestionnaireService.get_questionnaires(
        db_session, category="security"
    )
    
    assert total == 1
    assert questionnaires[0].category == "security"

def test_update_questionnaire(db_session):
    questionnaire_data = QuestionnaireCreate(
        title="Original Title",
        description="Original description"
    )
    created = QuestionnaireService.create_questionnaire(db_session, questionnaire_data)
    
    update_data = QuestionnaireUpdate(title="Updated Title")
    updated = QuestionnaireService.update_questionnaire(db_session, created.id, update_data)
    
    assert updated.title == "Updated Title"
    assert updated.description == "Original description"

def test_delete_questionnaire(db_session):
    questionnaire_data = QuestionnaireCreate(
        title="To Delete",
        description="Will be deleted"
    )
    created = QuestionnaireService.create_questionnaire(db_session, questionnaire_data)
    
    deleted = QuestionnaireService.delete_questionnaire(db_session, created.id)
    assert deleted is True
    
    retrieved = QuestionnaireService.get_questionnaire(db_session, created.id)
    assert retrieved is None
