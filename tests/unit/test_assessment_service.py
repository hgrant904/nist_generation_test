import pytest
from app.services import QuestionnaireService, QuestionService, AssessmentService
from app.schemas.questionnaire import QuestionnaireCreate
from app.schemas.question import QuestionCreate
from app.schemas.assessment import AssessmentSessionCreate, ResponseSubmit
from app.models.assessment_session import SessionStatus

@pytest.fixture
def sample_questionnaire(db_session):
    return QuestionnaireService.create_questionnaire(
        db_session,
        QuestionnaireCreate(title="Test Questionnaire", description="Test")
    )

@pytest.fixture
def sample_questions(db_session, sample_questionnaire):
    q1 = QuestionService.create_question(
        db_session,
        QuestionCreate(
            questionnaire_id=sample_questionnaire.id,
            question_text="Question 1",
            question_type="text",
            order_index=0
        )
    )
    
    q2 = QuestionService.create_question(
        db_session,
        QuestionCreate(
            questionnaire_id=sample_questionnaire.id,
            question_text="Question 2",
            question_type="yes_no",
            order_index=1
        )
    )
    
    return [q1, q2]

def test_start_assessment(db_session, sample_questionnaire):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id,
        user_id="user123"
    )
    
    session = AssessmentService.start_assessment(db_session, session_data)
    
    assert session.id is not None
    assert session.session_token is not None
    assert session.status == SessionStatus.IN_PROGRESS
    assert session.user_id == "user123"

def test_get_session(db_session, sample_questionnaire):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id
    )
    created = AssessmentService.start_assessment(db_session, session_data)
    
    retrieved = AssessmentService.get_session(db_session, created.session_token)
    
    assert retrieved is not None
    assert retrieved.id == created.id

def test_resolve_next_question(db_session, sample_questionnaire, sample_questions):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id
    )
    session = AssessmentService.start_assessment(db_session, session_data)
    
    next_question = AssessmentService.resolve_next_question(db_session, session)
    
    assert next_question is not None
    assert next_question.id == sample_questions[0].id

def test_submit_response(db_session, sample_questionnaire, sample_questions):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id
    )
    session = AssessmentService.start_assessment(db_session, session_data)
    
    response_data = ResponseSubmit(
        session_token=session.session_token,
        question_id=sample_questions[0].id,
        answer_value="Test answer"
    )
    
    response = AssessmentService.submit_response(db_session, response_data)
    
    assert response.id is not None
    assert response.answer_value == "Test answer"
    assert response.question_id == sample_questions[0].id

def test_submit_response_invalid_session(db_session, sample_questions):
    response_data = ResponseSubmit(
        session_token="invalid-token",
        question_id=sample_questions[0].id,
        answer_value="Test answer"
    )
    
    with pytest.raises(ValueError, match="Invalid session token"):
        AssessmentService.submit_response(db_session, response_data)

def test_submit_response_updates_existing(db_session, sample_questionnaire, sample_questions):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id
    )
    session = AssessmentService.start_assessment(db_session, session_data)
    
    response_data = ResponseSubmit(
        session_token=session.session_token,
        question_id=sample_questions[0].id,
        answer_value="First answer"
    )
    AssessmentService.submit_response(db_session, response_data)
    
    response_data.answer_value = "Updated answer"
    updated_response = AssessmentService.submit_response(db_session, response_data)
    
    assert updated_response.answer_value == "Updated answer"
    
    responses = AssessmentService.get_session_responses(db_session, session.id)
    assert len(responses) == 1

def test_evaluate_branching_rules():
    rules = [
        {"condition": "equals", "value": "yes", "next_question_id": 10},
        {"condition": "equals", "value": "no", "next_question_id": 20}
    ]
    
    next_id = AssessmentService.evaluate_branching_rules(rules, "yes")
    assert next_id == 10
    
    next_id = AssessmentService.evaluate_branching_rules(rules, "no")
    assert next_id == 20
    
    next_id = AssessmentService.evaluate_branching_rules(rules, "maybe")
    assert next_id is None

def test_session_completion(db_session, sample_questionnaire, sample_questions):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id
    )
    session = AssessmentService.start_assessment(db_session, session_data)
    
    for question in sample_questions:
        response_data = ResponseSubmit(
            session_token=session.session_token,
            question_id=question.id,
            answer_value="Answer"
        )
        AssessmentService.submit_response(db_session, response_data)
    
    updated_session = AssessmentService.get_session(db_session, session.session_token)
    assert updated_session.status == SessionStatus.COMPLETED
    assert updated_session.completed_at is not None

def test_get_answered_questions(db_session, sample_questionnaire, sample_questions):
    session_data = AssessmentSessionCreate(
        questionnaire_id=sample_questionnaire.id
    )
    session = AssessmentService.start_assessment(db_session, session_data)
    
    response_data = ResponseSubmit(
        session_token=session.session_token,
        question_id=sample_questions[0].id,
        answer_value="Answer 1"
    )
    AssessmentService.submit_response(db_session, response_data)
    
    answered = AssessmentService.get_answered_questions(db_session, session.id)
    
    assert len(answered) == 1
    assert answered[sample_questions[0].id] == "Answer 1"
