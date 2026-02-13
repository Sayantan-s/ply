from typing import Annotated, Any

from browser_use_sdk import AsyncBrowserUse
from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from google import genai
from qstash.client import QStash
from qstash.receiver import Receiver
from redis import asyncio as aioredis  # type: ignore
from sqlmodel import Session

from app.api.v1.dto.jdmatch import JdMatchResponse
from app.core.logging.logger import get_logger
from app.integrations.browser_use.agent import get_browser_use_client
from app.integrations.db.database import get_session
from app.integrations.llm.gemini import get_gemini_client
from app.integrations.redis.store import get_redis_store
from app.integrations.upstash.qstash import get_qstash_client, get_qstash_consumer
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.modules.jdmatch.service import jd_match, jd_match_consumer

router: APIRouter = APIRouter()

logger = get_logger("jdmatch.api")


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=JdMatchResponse)  # type: ignore[misc]
async def jdmatch(
    jd_info: Annotated[str, Form()],
    qstash: Annotated[QStash, Depends(get_qstash_client)],
    store: Annotated[aioredis.Redis, Depends(get_redis_store)],
    resume_file: UploadFile | None = None,
    resume_url: Annotated[str | None, Form()] = None,
) -> JdMatchResponse:
    logger.info("starting jdmatch()")
    response = await jd_match(resume_file, resume_url, jd_info, qstash, store)
    logger.info("ending jdmatch()")
    return response


@router.post("/consumer", status_code=status.HTTP_200_OK)  # type: ignore[misc]
async def jdmatch_consumer(
    req: Request,
    receiver: Annotated[Receiver, Depends(get_qstash_consumer)],
    store: Annotated[aioredis.Redis, Depends(get_redis_store)],
    gemini_client: Annotated[genai.Client, Depends(get_gemini_client)],
    session: Annotated[Session, Depends(get_session)],
    browser_use_client: Annotated[AsyncBrowserUse, Depends(get_browser_use_client)],
) -> dict[str, Any]:
    logger.info("starting jdmatch_consumer()")

    _body = await req.body()

    signature, req_body = req.headers["Upstash-Signature"], _body.decode()
    receiver.verify(body=req_body, signature=signature)

    payload = ParseResumeJDInformation.model_validate_json(req_body)
    await jd_match_consumer(payload, store, gemini_client, session, browser_use_client)
    logger.info("ending jdmatch_consumer()")

    return {"status": "received", "payload": payload}
