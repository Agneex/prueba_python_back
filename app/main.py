from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestLoggingMiddleware
from app.db.session import engine, init_db
from app.functions.router import router as functions_router
from app.users.auth_router import router as auth_router
from app.users.router import router as users_router

settings = get_settings()
configure_logging(settings.log_level, settings.log_json)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_db()
    logger.info("app_started", environment=settings.environment)
    yield
    await engine.dispose()
    logger.info("app_stopped")


app = FastAPI(title=settings.name, version="0.1.0", lifespan=lifespan)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(functions_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
