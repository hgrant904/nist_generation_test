from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import questionnaires_router, questions_router, assessments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NIST Questionnaire Engine API",
    description="""
    A comprehensive questionnaire engine API for NIST security report automation.
    
    Features:
    * **Questionnaires**: Create and manage questionnaires with versioning
    * **Questions**: Design questions with branching logic and dependencies
    * **Assessments**: Start sessions, submit responses, and track progress
    * **Branching Logic**: Dynamic question flow based on previous answers
    * **Session Management**: Resume incomplete assessments
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Questionnaires",
            "description": "Operations for managing questionnaires. Questionnaires are containers for organized sets of questions."
        },
        {
            "name": "Questions",
            "description": "Operations for managing questions within questionnaires. Supports multiple question types, branching rules, and dependencies."
        },
        {
            "name": "Assessments",
            "description": "Operations for conducting assessments. Start sessions, answer questions, and track completion with intelligent branching."
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questionnaires_router)
app.include_router(questions_router)
app.include_router(assessments_router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the NIST Questionnaire Engine API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
