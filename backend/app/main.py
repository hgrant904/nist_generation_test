"""FastAPI application factory and configuration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health
from app.core.logging_config import get_logger, setup_logging
from app.core.settings import settings
from app.db.session import engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    setup_logging()
    logger.info("Starting up %s v%s", settings.PROJECT_NAME, settings.VERSION)
    logger.info("Database URL: %s", settings.DATABASE_URL.split("@")[-1])
    yield
    logger.info("Shutting down %s", settings.PROJECT_NAME)
    await engine.dispose()


def create_app() -> FastAPI:
    """Application factory for creating FastAPI app instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.include_router(health.router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
