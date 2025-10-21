import pytest

def create_questionnaire_with_questions(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Assessment", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    q1_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "Question 1",
            "question_type": "text",
            "order_index": 0
        }
    )
    
    q2_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "Question 2",
            "question_type": "yes_no",
            "order_index": 1
        }
    )
    
    return questionnaire_id, [q1_response.json()["id"], q2_response.json()["id"]]

def test_start_assessment(client):
    questionnaire_id, _ = create_questionnaire_with_questions(client)
    
    response = client.post(
        "/api/assessments/start",
        json={
            "questionnaire_id": questionnaire_id,
            "user_id": "user123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["questionnaire_id"] == questionnaire_id
    assert data["user_id"] == "user123"
    assert data["status"] == "in_progress"
    assert "session_token" in data

def test_get_session(client):
    questionnaire_id, _ = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    response = client.get(f"/api/assessments/sessions/{session_token}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_token"] == session_token

def test_get_next_question(client):
    questionnaire_id, question_ids = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    response = client.get(f"/api/assessments/sessions/{session_token}/next-question")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question_ids[0]
    assert data["question_text"] == "Question 1"

def test_submit_response(client):
    questionnaire_id, question_ids = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    response = client.post(
        "/api/assessments/responses",
        json={
            "session_token": session_token,
            "question_id": question_ids[0],
            "answer_value": "Test answer"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["answer_value"] == "Test answer"
    assert data["question_id"] == question_ids[0]

def test_submit_response_invalid_session(client):
    response = client.post(
        "/api/assessments/responses",
        json={
            "session_token": "invalid-token",
            "question_id": 1,
            "answer_value": "Test"
        }
    )
    
    assert response.status_code == 400

def test_get_session_responses(client):
    questionnaire_id, question_ids = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    client.post(
        "/api/assessments/responses",
        json={
            "session_token": session_token,
            "question_id": question_ids[0],
            "answer_value": "Answer 1"
        }
    )
    
    response = client.get(f"/api/assessments/sessions/{session_token}/responses")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["answer_value"] == "Answer 1"

def test_complete_assessment_flow(client):
    questionnaire_id, question_ids = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    for question_id in question_ids:
        client.post(
            "/api/assessments/responses",
            json={
                "session_token": session_token,
                "question_id": question_id,
                "answer_value": "Answer"
            }
        )
    
    next_question_response = client.get(
        f"/api/assessments/sessions/{session_token}/next-question"
    )
    assert next_question_response.json() is None
    
    session_response = client.get(f"/api/assessments/sessions/{session_token}")
    assert session_response.json()["status"] == "completed"
    assert session_response.json()["completed_at"] is not None

def test_resume_session(client):
    questionnaire_id, _ = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    response = client.post(f"/api/assessments/sessions/{session_token}/resume")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"

def test_update_existing_response(client):
    questionnaire_id, question_ids = create_questionnaire_with_questions(client)
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    client.post(
        "/api/assessments/responses",
        json={
            "session_token": session_token,
            "question_id": question_ids[0],
            "answer_value": "First answer"
        }
    )
    
    client.post(
        "/api/assessments/responses",
        json={
            "session_token": session_token,
            "question_id": question_ids[0],
            "answer_value": "Updated answer"
        }
    )
    
    responses = client.get(f"/api/assessments/sessions/{session_token}/responses")
    data = responses.json()
    
    assert len(data) == 1
    assert data[0]["answer_value"] == "Updated answer"

def test_branching_logic_flow(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Branching Test", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    q1_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "Do you have a security team?",
            "question_type": "yes_no",
            "order_index": 0
        }
    )
    q1_id = q1_response.json()["id"]
    
    q2_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "How many team members?",
            "question_type": "number",
            "order_index": 1,
            "depends_on_question_id": q1_id,
            "depends_on_answer": "yes"
        }
    )
    q2_id = q2_response.json()["id"]
    
    start_response = client.post(
        "/api/assessments/start",
        json={"questionnaire_id": questionnaire_id}
    )
    session_token = start_response.json()["session_token"]
    
    client.post(
        "/api/assessments/responses",
        json={
            "session_token": session_token,
            "question_id": q1_id,
            "answer_value": "yes"
        }
    )
    
    next_question = client.get(
        f"/api/assessments/sessions/{session_token}/next-question"
    )
    assert next_question.json()["id"] == q2_id
