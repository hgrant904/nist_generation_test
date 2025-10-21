from __future__ import annotations

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import get_settings


async def generate_chat_completion(message: str, context: list[str] | None = None) -> str:
    settings = get_settings()

    if settings.llm_provider.lower() != "ollama":
        raise ValueError("Only the Ollama provider is currently supported")

    model = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.ollama_temperature,
    )

    prompt_messages: list[SystemMessage | HumanMessage] = []

    if context:
        context_blob = "\n".join(context)
        prompt_messages.append(
            SystemMessage(
                content=(
                    "You are a cybersecurity analyst helping organizations assess their maturity "
                    "against the NIST Cybersecurity Framework. Use the provided context when "
                    "available."
                )
            )
        )
        prompt_messages.append(SystemMessage(content=f"Context:\n{context_blob}"))

    prompt_messages.append(HumanMessage(content=message))

    response = await model.ainvoke(prompt_messages)
    return response.content
