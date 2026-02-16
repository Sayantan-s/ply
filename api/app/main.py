from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, Response
from scalar_fastapi import get_scalar_api_reference

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging.middleware import request_id_middleware
from app.integrations.db.database import connect_to_postgres
from app.integrations.redis.store import connect_to_redis


@asynccontextmanager
async def server_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
    connect_to_postgres()
    await connect_to_redis()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=server_lifespan,
    openapi_url=settings.OPENAPI_URL,
    docs_url=None,
)


@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> Any:
    return get_scalar_api_reference(
        title=settings.APP_NAME,
        openapi_url=app.openapi_url,
        scalar_proxy_url="https://proxy.scalar.com",
    )


@app.middleware("http")
async def middleware(request: Request, call_next: Callable[[Request], Any]) -> Response:
    return await request_id_middleware(request, call_next)


app.include_router(api_router, prefix="/api/v1")
