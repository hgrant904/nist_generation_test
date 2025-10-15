from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse
from src.database.connection import get_session
from src.models.schemas import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
    HealthCheckResponse,
    ErrorResponse,
)
from src.services.conversation_service import conversation_service
from src.services.ollama_service import ollama_service
from datetime import datetime, timezone
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_session),
):
    try:
        response = await conversation_service.chat(
            db=db,
            session_id=request.session_id,
            user_message=request.message,
            include_questionnaire_context=request.include_context,
        )
        
        return ChatResponse(
            session_id=request.session_id,
            message=response,
            timestamp=datetime.now(timezone.utc),
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message. Please ensure Ollama is running. Error: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_session),
):
    async def event_generator():
        try:
            async for chunk in conversation_service.chat_stream(
                db=db,
                session_id=request.session_id,
                user_message=request.message,
                include_questionnaire_context=request.include_context,
            ):
                yield {
                    "event": "message",
                    "data": json.dumps({"content": chunk})
                }
            
            yield {
                "event": "done",
                "data": json.dumps({"status": "complete"})
            }
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


@router.get("/chat/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    db: AsyncSession = Depends(get_session),
):
    try:
        messages = await conversation_service.get_chat_history(db, session_id)
        return ChatHistoryResponse(
            session_id=session_id,
            messages=messages,
        )
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve chat history: {str(e)}"
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    health_status = await ollama_service.check_health()
    
    if health_status["status"] == "unhealthy":
        return HealthCheckResponse(**health_status)
    
    return HealthCheckResponse(**health_status)
