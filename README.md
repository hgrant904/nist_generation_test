# NIST Automation MVP

Automate NIST security report generation for end users.

This repository contains an MVP monorepo structure with a FastAPI backend and Docker Compose wiring for Postgres and an Ollama LLM service.

- Backend: ./backend
- Compose: docker-compose.yml (services: db, backend, ollama)

Quick start:

1) Copy environment template and start services

```
cp backend/.env.example backend/.env
docker compose up --build
```

2) Open http://localhost:8000/docs to explore the API.
