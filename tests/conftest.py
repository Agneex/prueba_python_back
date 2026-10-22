from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_session, init_db
from app.main import app


@pytest.fixture
async def session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    test_database_url = get_settings().test_database_url
    if not test_database_url:
        pytest.exit("Define APP_TEST_DATABASE_URL para ejecutar los tests", returncode=2)

    test_engine = create_async_engine(test_database_url, poolclass=NullPool)
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await init_db(test_engine)
    yield async_sessionmaker(test_engine, expire_on_commit=False)
    await test_engine.dispose()


@pytest.fixture
async def db_session(session_factory) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client(session_factory) -> AsyncIterator[AsyncClient]:
    async def override_get_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client
    app.dependency_overrides.clear()
