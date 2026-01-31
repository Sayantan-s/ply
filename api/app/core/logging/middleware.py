import uuid

from fastapi import Request

from app.core.logging.logger import get_logger

logger = get_logger("middleware")


async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    logger.bind(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
    ).info("request_completed")

    return response
