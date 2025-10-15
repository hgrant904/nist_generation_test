import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.ollama_service import OllamaService
from langchain_core.messages import HumanMessage, AIMessage


@pytest.fixture
def ollama_service():
    return OllamaService()


def test_ollama_service_initialization(ollama_service):
    assert ollama_service.base_url == "http://localhost:11434"
    assert ollama_service.model == "llama3.1:8b"
    assert ollama_service.temperature == 0.7
    assert ollama_service.num_predict == 512


def test_get_session_history_creates_new(ollama_service):
    session_id = "test-session-1"
    history = ollama_service._get_session_history(session_id)
    
    assert session_id in ollama_service.store
    assert history is not None


def test_get_session_history_returns_existing(ollama_service):
    session_id = "test-session-2"
    history1 = ollama_service._get_session_history(session_id)
    history1.add_message(HumanMessage(content="Test"))
    
    history2 = ollama_service._get_session_history(session_id)
    assert history1 is history2
    assert len(history2.messages) == 1


def test_load_chat_history(ollama_service):
    session_id = "test-session-3"
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    
    ollama_service.load_chat_history(session_id, messages)
    history = ollama_service._get_session_history(session_id)
    
    assert len(history.messages) == 2
    assert isinstance(history.messages[0], HumanMessage)
    assert isinstance(history.messages[1], AIMessage)
    assert history.messages[0].content == "Hello"
    assert history.messages[1].content == "Hi there!"


def test_clear_session_history(ollama_service):
    session_id = "test-session-4"
    ollama_service._get_session_history(session_id)
    assert session_id in ollama_service.store
    
    ollama_service.clear_session_history(session_id)
    assert session_id not in ollama_service.store


@pytest.mark.asyncio
async def test_check_health_success(ollama_service):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "llama3.1:8b"},
            {"name": "mistral:7b"},
        ]
    }
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        result = await ollama_service.check_health()
        
        assert result["status"] == "healthy"
        assert result["ollama_available"] is True
        assert result["model_available"] is True


@pytest.mark.asyncio
async def test_check_health_model_not_found(ollama_service):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "mistral:7b"},
        ]
    }
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        result = await ollama_service.check_health()
        
        assert result["status"] == "degraded"
        assert result["ollama_available"] is True
        assert result["model_available"] is False


@pytest.mark.asyncio
async def test_check_health_connection_error(ollama_service):
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("Connection refused"))
        
        result = await ollama_service.check_health()
        
        assert result["status"] == "unhealthy"
        assert result["ollama_available"] is False
        assert "error" in result
