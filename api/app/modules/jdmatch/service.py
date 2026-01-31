from fastapi import UploadFile
from qstash.client import QStash
from redis import asyncio as aioredis

from app.core.config import settings
from app.core.logging.logger import get_logger
from app.modules.jdmatch.constants import JdMatchStatus
from app.modules.jdmatch.repo import (
    init_file,
    init_file_identity,
    save_file,
)
from app.modules.jdmatch.schemas import ParseResumeJDInformation

# qstash_dependency removed since it's passed from API layer

logger = get_logger("jdmatch.service")


async def jd_match(
    resume_file: UploadFile | None = None,
    resume_url: str | None = None,
    jd_info: str = None,
    qstash: QStash = None,
    store: aioredis.Redis = None,
):
    logger.info("starting jd_match()")

    file_id = init_file_identity(resume_url)

    await store.set(f"jdmatch:{file_id}", JdMatchStatus.PARSING.value)

    file_content, filename, file_id = await init_file(
        resume_file, resume_url, file_id=file_id
    )

    resume_info = save_file(file_content, jd_info, filename, file_id)

    target_url = f"{settings.API_URL}/jdmatch/consumer"

    qstash.message.publish_json(
        url=target_url,
        body=resume_info.model_dump(),
    )

    await store.set(f"jdmatch:{file_id}", JdMatchStatus.QUEUED.value)

    logger.info("ending jd_match()")

    return file_id


async def jd_match_consumer(
    payload: ParseResumeJDInformation, store: aioredis.Redis = None
):
    logger.info("starting jd_match_consumer()")

    file_id = payload.file_name.split("-")[0]

    await store.set(f"jdmatch:{file_id}", JdMatchStatus.PROCESSING.value)

    logger.info("ending jd_match_consumer()")
