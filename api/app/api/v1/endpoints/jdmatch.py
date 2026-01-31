from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from qstash.client import QStash
from qstash.receiver import Receiver
from redis import asyncio as aioredis

from app.api.v1.dto.jdmatch import JdMatchResponse
from app.core.logging.logger import get_logger
from app.integrations.redis.store import get_redis_store
from app.integrations.upstash.qstash import get_qstash_client, get_qstash_consumer
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.modules.jdmatch.service import jd_match, jd_match_consumer

router = APIRouter()

logger = get_logger("jdmatch.api")


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=JdMatchResponse)
async def jdmatch(
    resume_file: UploadFile | None = None,
    resume_url: str | None = Form(None),
    jd_info: str = Form(...),
    qstash: QStash = Depends(get_qstash_client),
    store: aioredis.Redis = Depends(get_redis_store),
):
    logger.info("starting jdmatch()")
    response = await jd_match(resume_file, resume_url, jd_info, qstash, store)
    logger.info("ending jdmatch()")
    return response


@router.post("/consumer", status_code=status.HTTP_200_OK)
async def jdmatch_consumer(
    req: Request,
    receiver: Receiver = Depends(get_qstash_consumer),
    store: aioredis.Redis = Depends(get_redis_store),
):
    logger.info("starting jdmatch_consumer()")

    _body = await req.body()

    signature, req_body = req.headers["Upstash-Signature"], _body.decode()
    receiver.verify(body=req_body, signature=signature)

    payload = ParseResumeJDInformation.model_validate_json(req_body)
    await jd_match_consumer(payload, store)
    logger.info("ending jdmatch_consumer()")

    return {"status": "received", "payload": payload}
