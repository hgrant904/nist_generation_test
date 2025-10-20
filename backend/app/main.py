from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": settings.app_name, "status": "running"}


@app.get("/health")
async def health_check():
    # Optionally try contacting the Ollama server; ignore errors for a soft check
    ollama_url = f"{settings.ollama_host}:{settings.ollama_port}/api/tags"
    ollama_reachable = False
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            resp = await client.get(ollama_url)
            ollama_reachable = resp.status_code == 200
    except Exception:
        ollama_reachable = False

    return {
        "status": "healthy",
        "ollama": {
            "host": settings.ollama_host,
            "port": settings.ollama_port,
            "model": settings.ollama_model,
            "reachable": ollama_reachable,
        },
    }
