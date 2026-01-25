from fastapi import FastAPI, Request
from app.api.v1.api import api_router
from app.core.logging.middleware import request_id_middleware

app = FastAPI(title="Ply Assistant APIs")

@app.middleware("http")
async def middleware(request: Request, call_next):
    return await request_id_middleware(request, call_next)

app.include_router(
    api_router,
    prefix="/api/v1"
)