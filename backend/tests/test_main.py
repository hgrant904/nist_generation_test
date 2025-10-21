from __future__ import annotations

from uuid import UUID

import pytest
from httpx import AsyncClient

from app.services import ollama


@pytest.mark.anyio
async def test_health_endpoint(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"


@pytest.mark.anyio
async def test_assessment_lifecycle(client: AsyncClient) -> None:
    start_response = await client.post("/assessments", json={"name": "Unit Test Assessment"})
    assert start_response.status_code == 201
    start_payload = start_response.json()

    assessment_id = UUID(start_payload["assessment_id"])
    first_question = start_payload["first_question"]
    assert first_question is not None

    submission = await client.post(
        f"/assessments/{assessment_id}/responses",
        json={
            "question_id": first_question["id"],
            "answer": "We maintain inventories quarterly",
        },
    )
    assert submission.status_code == 201

    progress = await client.get(f"/assessments/{assessment_id}/progress")
    assert progress.status_code == 200
    progress_payload = progress.json()
    assert progress_payload["answered_questions"] == 1
    assert progress_payload["total_questions"] > 1

    next_question_response = await client.get(f"/assessments/{assessment_id}/next-question")
    assert next_question_response.status_code == 200
    next_payload = next_question_response.json()
    assert next_payload["question"] is not None
    assert next_payload["remaining_questions"] >= 0

    responses_response = await client.get(f"/assessments/{assessment_id}/responses")
    assert responses_response.status_code == 200
    responses_payload = responses_response.json()
    assert len(responses_payload) == 1
    assert responses_payload[0]["answer"] == "We maintain inventories quarterly"


@pytest.mark.anyio
async def test_questions_listing(client: AsyncClient) -> None:
    response = await client.get("/questions")
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) >= 1
    assert {"id", "code", "prompt"}.issubset(questions[0].keys())

    functions_response = await client.get("/questions/functions")
    assert functions_response.status_code == 200
    assert len(functions_response.json()) == 5


@pytest.mark.anyio
async def test_chat_endpoint(monkeypatch: pytest.MonkeyPatch, client: AsyncClient) -> None:
    async def _fake_generate(message: str, context: list[str] | None = None) -> str:
        return f"echo: {message}"

    monkeypatch.setattr(ollama, "generate_chat_completion", _fake_generate)

    response = await client.post("/chat", json={"message": "hello"})
    assert response.status_code == 200
    assert response.json()["response"] == "echo: hello"
