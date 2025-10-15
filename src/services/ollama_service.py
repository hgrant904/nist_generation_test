import httpx
from typing import Optional, AsyncGenerator
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaService:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.temperature = settings.ollama_temperature
        self.num_predict = settings.ollama_num_predict
        self.store = {}
        
    def _get_llm(self, streaming: bool = False):
        return ChatOllama(
            base_url=self.base_url,
            model=self.model,
            temperature=self.temperature,
            num_predict=self.num_predict,
            streaming=streaming,
        )
    
    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def create_conversation_chain(self, system_prompt: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        llm = self._get_llm(streaming=False)
        chain = prompt | llm
        
        return RunnableWithMessageHistory(
            chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
    
    def create_streaming_conversation_chain(self, system_prompt: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        llm = self._get_llm(streaming=True)
        chain = prompt | llm
        
        return RunnableWithMessageHistory(
            chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
    
    async def check_health(self) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                
                if response.status_code != 200:
                    return {
                        "status": "unhealthy",
                        "ollama_available": False,
                        "error": f"Ollama returned status {response.status_code}"
                    }
                
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                model_available = any(self.model in name for name in model_names)
                
                return {
                    "status": "healthy" if model_available else "degraded",
                    "ollama_available": True,
                    "model_available": model_available,
                    "configured_model": self.model,
                    "available_models": model_names,
                }
        except httpx.ConnectError:
            logger.error(f"Failed to connect to Ollama at {self.base_url}")
            return {
                "status": "unhealthy",
                "ollama_available": False,
                "error": f"Cannot connect to Ollama at {self.base_url}. Ensure Ollama is running."
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "ollama_available": False,
                "error": str(e)
            }
    
    def load_chat_history(self, session_id: str, messages: list):
        history = self._get_session_history(session_id)
        history.clear()
        
        for msg in messages:
            if msg["role"] == "user":
                history.add_message(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                history.add_message(AIMessage(content=msg["content"]))
    
    def clear_session_history(self, session_id: str):
        if session_id in self.store:
            del self.store[session_id]


ollama_service = OllamaService()
