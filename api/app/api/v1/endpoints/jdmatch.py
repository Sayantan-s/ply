from typing import Annotated, Any

from browser_use_sdk import AsyncBrowserUse
from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from google import genai
from qstash.client import QStash
from qstash.receiver import Receiver
from redis import asyncio as aioredis
from sqlmodel import Session

from app.api.v1.dto.jdmatch import JdMatchResponse, JdResponse, ResumeUploadResponse
from app.core.logging.logger import get_logger
from app.integrations.browser_use.agent import get_browser_use_client
from app.integrations.db.database import get_session
from app.integrations.llm.gemini import get_gemini_client
from app.integrations.redis.store import get_redis_store
from app.integrations.upstash.qstash import get_qstash_client, get_qstash_consumer
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.modules.jdmatch.service import (
    jd_match_analyze,
    jd_match_init,
    process_jd,
    upload_resume,
)

router: APIRouter = APIRouter()

logger = get_logger("jdmatch.api")


@router.post("/resume/upload", status_code=status.HTTP_201_CREATED, response_model=ResumeUploadResponse)
async def upload_resume_endpoint(
    session: Annotated[Session, Depends(get_session)],
    resume_file: UploadFile | None = None,
    resume_url: Annotated[str | None, Form()] = None,
) -> ResumeUploadResponse:
    logger.info("starting upload_resume_endpoint()")
    response = await upload_resume(session, resume_file, resume_url)
    logger.info("ending upload_resume_endpoint()")
    return response


@router.patch("/{file_id}/jd/add", status_code=status.HTTP_200_OK, response_model=JdResponse)
async def add_jd_endpoint(
    file_id: str,
    jd_info: Annotated[str, Form()],
    session: Annotated[Session, Depends(get_session)],
) -> JdResponse:
    logger.info(f"starting add_jd_endpoint for {file_id}")
    response = await process_jd(session, file_id, jd_info)
    logger.info(f"ending add_jd_endpoint for {file_id}")
    return response


@router.post("/{file_id}/init", status_code=status.HTTP_202_ACCEPTED, response_model=JdMatchResponse)
async def jdmatch_init_endpoint(
    file_id: str,
    qstash: Annotated[QStash, Depends(get_qstash_client)],
    store: Annotated[aioredis.Redis, Depends(get_redis_store)],
    session: Annotated[Session, Depends(get_session)],
) -> JdMatchResponse:
    logger.info(f"starting jdmatch_init_endpoint for {file_id}")
    response = await jd_match_init(file_id, qstash, store, session)
    logger.info(f"ending jdmatch_init_endpoint for {file_id}")
    return response


@router.post("/consumer", status_code=status.HTTP_200_OK)
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
    await jd_match_analyze(payload, store, gemini_client, session, browser_use_client)
    logger.info("ending jdmatch_consumer()")

    return {"status": "received", "payload": payload}
