from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime
from src.database.models import Conversation, Message, QuestionnaireResponse
from src.services.ollama_service import ollama_service
from src.prompts.system_prompts import get_system_prompt_with_context, format_questionnaire_context
import logging

logger = logging.getLogger(__name__)


class ConversationService:
    async def create_conversation(self, db: AsyncSession, session_id: Optional[str] = None) -> Conversation:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        conversation = Conversation(session_id=session_id)
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation
    
    async def get_conversation(self, db: AsyncSession, session_id: str) -> Optional[Conversation]:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.session_id == session_id)
            .options(selectinload(Conversation.messages))
        )
        return result.scalar_one_or_none()
    
    async def save_message(self, db: AsyncSession, conversation_id: int, role: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message
    
    async def get_chat_history(self, db: AsyncSession, session_id: str) -> list:
        conversation = await self.get_conversation(db, session_id)
        if not conversation:
            return []
        
        messages = sorted(conversation.messages, key=lambda m: m.timestamp)
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in messages
        ]
    
    async def get_questionnaire_context(self, db: AsyncSession, session_id: str) -> str:
        result = await db.execute(
            select(QuestionnaireResponse)
            .where(QuestionnaireResponse.session_id == session_id)
            .order_by(QuestionnaireResponse.created_at)
        )
        responses = result.scalars().all()
        
        if not responses:
            return ""
        
        response_dicts = [
            {
                "category": r.category,
                "question": r.question,
                "answer": r.answer,
            }
            for r in responses
        ]
        
        return format_questionnaire_context(response_dicts)
    
    async def chat(
        self,
        db: AsyncSession,
        session_id: str,
        user_message: str,
        include_questionnaire_context: bool = True,
    ) -> str:
        conversation = await self.get_conversation(db, session_id)
        if not conversation:
            conversation = await self.create_conversation(db, session_id)
        
        questionnaire_context = ""
        if include_questionnaire_context:
            questionnaire_context = await self.get_questionnaire_context(db, session_id)
        
        system_prompt = get_system_prompt_with_context(questionnaire_context)
        
        chat_history = await self.get_chat_history(db, session_id)
        ollama_service.load_chat_history(session_id, chat_history)
        
        chain = ollama_service.create_conversation_chain(system_prompt)
        
        try:
            response = await chain.ainvoke(
                {"input": user_message},
                config={"configurable": {"session_id": session_id}}
            )
            
            assistant_message = response.content
            
            await self.save_message(db, conversation.id, "user", user_message)
            await self.save_message(db, conversation.id, "assistant", assistant_message)
            
            return assistant_message
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise
    
    async def chat_stream(
        self,
        db: AsyncSession,
        session_id: str,
        user_message: str,
        include_questionnaire_context: bool = True,
    ) -> AsyncGenerator[str, None]:
        conversation = await self.get_conversation(db, session_id)
        if not conversation:
            conversation = await self.create_conversation(db, session_id)
        
        questionnaire_context = ""
        if include_questionnaire_context:
            questionnaire_context = await self.get_questionnaire_context(db, session_id)
        
        system_prompt = get_system_prompt_with_context(questionnaire_context)
        
        chat_history = await self.get_chat_history(db, session_id)
        ollama_service.load_chat_history(session_id, chat_history)
        
        chain = ollama_service.create_streaming_conversation_chain(system_prompt)
        
        try:
            full_response = ""
            async for chunk in chain.astream(
                {"input": user_message},
                config={"configurable": {"session_id": session_id}}
            ):
                content = chunk.content
                full_response += content
                yield content
            
            await self.save_message(db, conversation.id, "user", user_message)
            await self.save_message(db, conversation.id, "assistant", full_response)
        except Exception as e:
            logger.error(f"Error in chat stream: {str(e)}")
            raise


conversation_service = ConversationService()
