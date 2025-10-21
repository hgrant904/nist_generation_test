import pytest

def test_create_question(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "What is your organization size?",
            "question_type": "multiple_choice",
            "options": ["Small", "Medium", "Large"],
            "order_index": 0
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["question_text"] == "What is your organization size?"
    assert data["question_type"] == "multiple_choice"
    assert len(data["options"]) == 3

def test_create_question_with_branching(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "Do you have a security team?",
            "question_type": "yes_no",
            "branching_rules": [
                {"condition": "equals", "value": "yes", "next_question_id": 10}
            ]
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert len(data["branching_rules"]) == 1

def test_get_questions_by_questionnaire(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    for i in range(3):
        client.post(
            "/api/questions/",
            json={
                "questionnaire_id": questionnaire_id,
                "question_text": f"Question {i}",
                "question_type": "text",
                "order_index": i
            }
        )
    
    response = client.get(f"/api/questions/questionnaire/{questionnaire_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_get_question_by_id(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    create_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "Test question",
            "question_type": "text"
        }
    )
    question_id = create_response.json()["id"]
    
    response = client.get(f"/api/questions/{question_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question_id

def test_update_question(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    create_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "Original question",
            "question_type": "text"
        }
    )
    question_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/questions/{question_id}",
        json={"question_text": "Updated question"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["question_text"] == "Updated question"

def test_delete_question(client):
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = questionnaire_response.json()["id"]
    
    create_response = client.post(
        "/api/questions/",
        json={
            "questionnaire_id": questionnaire_id,
            "question_text": "To delete",
            "question_type": "text"
        }
    )
    question_id = create_response.json()["id"]
    
    response = client.delete(f"/api/questions/{question_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/api/questions/{question_id}")
    assert get_response.status_code == 404
