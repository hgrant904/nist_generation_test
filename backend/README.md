# Backend (FastAPI)

This is a minimal FastAPI backend for the NIST automation MVP. It exposes a simple health endpoint and is wired for Postgres and an Ollama LLM service.

## Quick start

1) Copy the environment template and adjust as needed:

```
cp backend/.env.example backend/.env
```

2) Start the stack with Docker Compose from the repo root:

```
docker compose up --build
```

3) Visit the API:

- Health check: http://localhost:8000/health
- Root: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs

## Environment variables

- POSTGRES_* variables configure the Postgres database
- OLLAMA_* variables configure the Ollama LLM service

The Ollama service is included in the `docker-compose.yml` and exposed on port 11434. The backend checks the Ollama service in the `/health` endpoint and returns whether it is reachable.

## Development

Install dependencies locally (optional):

```
pip install -r backend/requirements.txt
uvicorn app.main:app --reload
```

