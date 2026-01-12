from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.logging.middleware import request_id_middleware

app = FastAPI(title="Ply Assistant APIs")

app.middleware("http")(request_id_middleware)

app.include_router(
    api_router,
    prefix="/api/v1"
)