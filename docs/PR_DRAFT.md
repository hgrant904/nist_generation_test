Title: Integration MVP for Tasks 1–5 (backend + compose + Ollama wiring)

Summary
- Establishes a runnable integration baseline with Docker Compose wiring for Postgres, Ollama, and FastAPI backend.
- Adds backend/.env.example including OLLAMA_* variables and DB settings.
- Provides health endpoint that reports Ollama reachability.

Merged/Incorporated
- Monorepo scaffolding (compose + backend skeleton)
- Backend init with app factory patterns (consolidated into app/main.py and core/settings.py)

Deferred for follow-up PRs
- Full NIST models/migrations/seeds integration (Alembic merge heads if needed)
- Questionnaire engine APIs + persistence
- Conversation agent APIs using Ollama

Local smoke test
- docker compose up --build
- GET /health -> 200 OK; returns status and Ollama connectivity flag

Notes
- This establishes the base for subsequent merging of application-specific features. Alembic configuration is in place under backend/alembic for future migrations.
