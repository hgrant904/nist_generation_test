import pytest

def test_create_questionnaire(client):
    response = client.post(
        "/api/questionnaires/",
        json={
            "title": "NIST Security Assessment",
            "description": "Comprehensive security assessment",
            "category": "security",
            "version": "1.0"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "NIST Security Assessment"
    assert data["category"] == "security"
    assert "id" in data

def test_get_questionnaires_list(client):
    client.post(
        "/api/questionnaires/",
        json={"title": "Test 1", "description": "Desc 1"}
    )
    client.post(
        "/api/questionnaires/",
        json={"title": "Test 2", "description": "Desc 2"}
    )
    
    response = client.get("/api/questionnaires/?page=1&page_size=10")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["page"] == 1

def test_get_questionnaires_with_filter(client):
    client.post(
        "/api/questionnaires/",
        json={"title": "Security Q", "category": "security"}
    )
    client.post(
        "/api/questionnaires/",
        json={"title": "Privacy Q", "category": "privacy"}
    )
    
    response = client.get("/api/questionnaires/?category=security")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category"] == "security"

def test_get_questionnaire_by_id(client):
    create_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test Questionnaire", "description": "Test"}
    )
    questionnaire_id = create_response.json()["id"]
    
    response = client.get(f"/api/questionnaires/{questionnaire_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == questionnaire_id
    assert data["title"] == "Test Questionnaire"

def test_get_questionnaire_not_found(client):
    response = client.get("/api/questionnaires/9999")
    assert response.status_code == 404

def test_update_questionnaire(client):
    create_response = client.post(
        "/api/questionnaires/",
        json={"title": "Original Title", "description": "Original"}
    )
    questionnaire_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/questionnaires/{questionnaire_id}",
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original"

def test_delete_questionnaire(client):
    create_response = client.post(
        "/api/questionnaires/",
        json={"title": "To Delete", "description": "Will be deleted"}
    )
    questionnaire_id = create_response.json()["id"]
    
    response = client.delete(f"/api/questionnaires/{questionnaire_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/api/questionnaires/{questionnaire_id}")
    assert get_response.status_code == 404

def test_pagination(client):
    for i in range(15):
        client.post(
            "/api/questionnaires/",
            json={"title": f"Questionnaire {i}", "description": f"Desc {i}"}
        )
    
    response = client.get("/api/questionnaires/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["total_pages"] == 2
    
    response = client.get("/api/questionnaires/?page=2&page_size=10")
    data = response.json()
    assert len(data["items"]) == 5
