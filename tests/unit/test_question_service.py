import pytest
from app.services import QuestionnaireService, QuestionService
from app.schemas.questionnaire import QuestionnaireCreate
from app.schemas.question import QuestionCreate, QuestionUpdate

@pytest.fixture
def sample_questionnaire(db_session):
    return QuestionnaireService.create_questionnaire(
        db_session,
        QuestionnaireCreate(title="Test Questionnaire", description="Test")
    )

def test_create_question(db_session, sample_questionnaire):
    question_data = QuestionCreate(
        questionnaire_id=sample_questionnaire.id,
        question_text="What is your organization size?",
        question_type="multiple_choice",
        options=["Small", "Medium", "Large"],
        order_index=1
    )
    
    question = QuestionService.create_question(db_session, question_data)
    
    assert question.id is not None
    assert question.question_text == "What is your organization size?"
    assert question.question_type == "multiple_choice"
    assert len(question.options) == 3

def test_create_question_with_branching(db_session, sample_questionnaire):
    question_data = QuestionCreate(
        questionnaire_id=sample_questionnaire.id,
        question_text="Do you have a security team?",
        question_type="yes_no",
        branching_rules=[
            {"condition": "equals", "value": "yes", "next_question_id": 10}
        ]
    )
    
    question = QuestionService.create_question(db_session, question_data)
    
    assert question.branching_rules is not None
    assert len(question.branching_rules) == 1

def test_get_question(db_session, sample_questionnaire):
    question_data = QuestionCreate(
        questionnaire_id=sample_questionnaire.id,
        question_text="Test question",
        question_type="text"
    )
    created = QuestionService.create_question(db_session, question_data)
    
    retrieved = QuestionService.get_question(db_session, created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id

def test_get_questions_by_questionnaire(db_session, sample_questionnaire):
    for i in range(3):
        QuestionService.create_question(
            db_session,
            QuestionCreate(
                questionnaire_id=sample_questionnaire.id,
                question_text=f"Question {i}",
                question_type="text",
                order_index=i
            )
        )
    
    questions, total = QuestionService.get_questions_by_questionnaire(
        db_session, sample_questionnaire.id
    )
    
    assert total == 3
    assert len(questions) == 3

def test_validate_dependencies_no_dependency(db_session, sample_questionnaire):
    question_data = QuestionCreate(
        questionnaire_id=sample_questionnaire.id,
        question_text="Independent question",
        question_type="text"
    )
    question = QuestionService.create_question(db_session, question_data)
    
    is_valid = QuestionService.validate_dependencies(db_session, question, {})
    assert is_valid is True

def test_validate_dependencies_with_dependency(db_session, sample_questionnaire):
    parent_question = QuestionService.create_question(
        db_session,
        QuestionCreate(
            questionnaire_id=sample_questionnaire.id,
            question_text="Parent question",
            question_type="yes_no"
        )
    )
    
    child_question = QuestionService.create_question(
        db_session,
        QuestionCreate(
            questionnaire_id=sample_questionnaire.id,
            question_text="Child question",
            question_type="text",
            depends_on_question_id=parent_question.id,
            depends_on_answer="yes"
        )
    )
    
    is_valid = QuestionService.validate_dependencies(
        db_session,
        child_question,
        {parent_question.id: "yes"}
    )
    assert is_valid is True
    
    is_invalid = QuestionService.validate_dependencies(
        db_session,
        child_question,
        {parent_question.id: "no"}
    )
    assert is_invalid is False

def test_update_question(db_session, sample_questionnaire):
    question_data = QuestionCreate(
        questionnaire_id=sample_questionnaire.id,
        question_text="Original question",
        question_type="text"
    )
    created = QuestionService.create_question(db_session, question_data)
    
    update_data = QuestionUpdate(question_text="Updated question")
    updated = QuestionService.update_question(db_session, created.id, update_data)
    
    assert updated.question_text == "Updated question"
    assert updated.question_type == "text"

def test_delete_question(db_session, sample_questionnaire):
    question_data = QuestionCreate(
        questionnaire_id=sample_questionnaire.id,
        question_text="To delete",
        question_type="text"
    )
    created = QuestionService.create_question(db_session, question_data)
    
    deleted = QuestionService.delete_question(db_session, created.id)
    assert deleted is True
    
    retrieved = QuestionService.get_question(db_session, created.id)
    assert retrieved is None
