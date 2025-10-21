from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User prompt to send to the Ollama model")
    context: list[str] | None = Field(
        default=None, description="Optional contextual strings to include in the prompt"
    )


class ChatResponse(BaseModel):
    response: str
