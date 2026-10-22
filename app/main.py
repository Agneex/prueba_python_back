from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app = FastAPI(title="Implicit Volumes API", version="0.1.0", lifespan=lifespan)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
