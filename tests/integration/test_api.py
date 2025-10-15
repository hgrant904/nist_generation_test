import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, Mock
from src.main import app
from src.database.connection import init_db, async_session_maker
from src.database.models import Base
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio


@pytest.fixture(scope="function")
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_health_endpoint_ollama_unavailable(client):
    with patch("src.services.ollama_service.ollama_service.check_health") as mock_health:
        mock_health.return_value = {
            "status": "unhealthy",
            "ollama_available": False,
            "error": "Cannot connect to Ollama"
        }
        
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["ollama_available"] is False


@pytest.mark.asyncio
async def test_health_endpoint_ollama_available(client):
    with patch("src.services.ollama_service.ollama_service.check_health") as mock_health:
        mock_health.return_value = {
            "status": "healthy",
            "ollama_available": True,
            "model_available": True,
            "configured_model": "llama3.1:8b",
            "available_models": ["llama3.1:8b"]
        }
        
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["ollama_available"] is True
        assert data["model_available"] is True


@pytest.mark.asyncio
async def test_chat_endpoint_success(client):
    mock_response = "This is a test response from the assistant."
    
    with patch("src.services.conversation_service.conversation_service.chat") as mock_chat:
        mock_chat.return_value = mock_response
        
        response = await client.post(
            "/api/v1/chat",
            json={
                "session_id": "test-session-123",
                "message": "Hello, what cloud services should I use?",
                "include_context": True,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-123"
        assert data["message"] == mock_response
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_chat_endpoint_error_handling(client):
    with patch("src.services.conversation_service.conversation_service.chat") as mock_chat:
        mock_chat.side_effect = Exception("Ollama connection failed")
        
        response = await client.post(
            "/api/v1/chat",
            json={
                "session_id": "test-session-456",
                "message": "Hello",
                "include_context": False,
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
async def test_get_chat_history_empty(client):
    with patch("src.services.conversation_service.conversation_service.get_chat_history") as mock_history:
        mock_history.return_value = []
        
        response = await client.get("/api/v1/chat/history/test-session-789")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-789"
        assert data["messages"] == []


@pytest.mark.asyncio
async def test_get_chat_history_with_messages(client):
    mock_messages = [
        {
            "role": "user",
            "content": "Hello",
            "timestamp": "2024-01-01T00:00:00",
        },
        {
            "role": "assistant",
            "content": "Hi! How can I help you?",
            "timestamp": "2024-01-01T00:00:01",
        }
    ]
    
    with patch("src.services.conversation_service.conversation_service.get_chat_history") as mock_history:
        mock_history.return_value = mock_messages
        
        response = await client.get("/api/v1/chat/history/test-session-999")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-999"
        assert len(data["messages"]) == 2
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][1]["role"] == "assistant"
