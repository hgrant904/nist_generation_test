import pytest
from src.services.ollama_service import ollama_service
from src.prompts.system_prompts import get_system_prompt_with_context


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ollama_health_check_live():
    result = await ollama_service.check_health()
    
    assert "status" in result
    assert "ollama_available" in result
    
    if result["ollama_available"]:
        assert result["status"] in ["healthy", "degraded"]
        if result["status"] == "degraded":
            pytest.skip("Ollama is running but llama3.1:8b model not found")
    else:
        pytest.skip("Ollama is not running, skipping live integration test")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ollama_conversation_live():
    health = await ollama_service.check_health()
    
    if not health.get("ollama_available") or not health.get("model_available"):
        pytest.skip("Ollama with llama3.1:8b not available")
    
    session_id = "test-live-session"
    ollama_service.clear_session_history(session_id)
    
    system_prompt = get_system_prompt_with_context()
    chain = ollama_service.create_conversation_chain(system_prompt)
    
    response = await chain.ainvoke(
        {"input": "Hello, I run a small accounting firm. Can you help me understand cloud security?"},
        config={"configurable": {"session_id": session_id}}
    )
    
    assert response is not None
    assert hasattr(response, "content")
    assert len(response.content) > 0
    assert isinstance(response.content, str)
    
    ollama_service.clear_session_history(session_id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ollama_streaming_live():
    health = await ollama_service.check_health()
    
    if not health.get("ollama_available") or not health.get("model_available"):
        pytest.skip("Ollama with llama3.1:8b not available")
    
    session_id = "test-live-streaming"
    ollama_service.clear_session_history(session_id)
    
    system_prompt = get_system_prompt_with_context()
    chain = ollama_service.create_streaming_conversation_chain(system_prompt)
    
    chunks = []
    async for chunk in chain.astream(
        {"input": "What is NIST CSF?"},
        config={"configurable": {"session_id": session_id}}
    ):
        chunks.append(chunk.content)
    
    assert len(chunks) > 0
    full_response = "".join(chunks)
    assert len(full_response) > 0
    
    ollama_service.clear_session_history(session_id)
