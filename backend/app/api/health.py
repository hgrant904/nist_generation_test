"""Health and status check endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.session import get_db
from app.schemas.health import DatabaseHealthResponse, HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Basic health check endpoint."""
    return HealthResponse(status="healthy", version=settings.VERSION)


@router.get("/health/db", response_model=DatabaseHealthResponse)
async def database_health_check(
    db: AsyncSession = Depends(get_db),
) -> DatabaseHealthResponse:
    """Database connectivity health check."""
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return DatabaseHealthResponse(database="postgresql", status="connected")
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Database connection failed: {str(e)}"
        )
