from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.models.base import Base

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.log_level.lower() == "debug",
    future=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Create database tables. Primarily used in testing contexts."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
