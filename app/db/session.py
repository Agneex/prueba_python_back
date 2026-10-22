from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.db.base import Base

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=settings.database_echo)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def init_db(db_engine: AsyncEngine = engine) -> None:
    from app.db import models  # noqa: F401  registra los modelos en el metadata

    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session
