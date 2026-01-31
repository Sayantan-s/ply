from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging.middleware import request_id_middleware
from app.integrations.db.database import init_db


@asynccontextmanager
async def lifespan():
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME)


@app.middleware("http")
async def middleware(request: Request, call_next):
    return await request_id_middleware(request, call_next)


app.include_router(api_router, prefix="/api/v1")
