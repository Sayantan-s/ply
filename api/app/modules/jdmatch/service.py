import json
import os

from browser_use_sdk import AsyncBrowserUse
from fastapi import UploadFile
from google import genai
from qstash.client import QStash
from redis import asyncio as aioredis
from sqlmodel import Session

from app.api.v1.dto.jdmatch import JdMatchResponse, ResumeUploadResponse
from app.core.config import settings
from app.core.logging.logger import get_logger
from app.integrations.supabase.storage import upload_file_to_supabase
from app.modules.jdmatch.agents.analyze_jd_text_structure import (
    agent_analyze_jd_text_structure,
)
from app.modules.jdmatch.agents.extract_jd import agent_extract_jd
from app.modules.jdmatch.agents.generate_candidate_score import (
    agent_generate_candidate_score,
)
from app.modules.jdmatch.constants import JdMatchStatus
from app.modules.jdmatch.repo import (
    create_jd_match_record,
    get_jd_match_by_jd_match_id,
    save_jd_match_info,
    update_jd_info,
)
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.modules.jdmatch.utils.cleanup_file import cleanup_file
from app.modules.jdmatch.utils.init_file import init_file
from app.modules.jdmatch.utils.init_file_identity import init_file_identity
from app.modules.jdmatch.utils.is_jd_link_or_description import (
    is_jd_link_or_description,
)

logger = get_logger("jdmatch.service")


async def upload_resume(
    _db_session: Session,
    resume_file: UploadFile | None = None,
    resume_url: str | None = None,
) -> ResumeUploadResponse:
    logger.info("starting upload_resume()")

    file_id = init_file_identity(resume_url or "")
    file_content, filename, file_id = await init_file(
        resume_file, resume_url, file_id=file_id
    )

    # Upload file to Storage
    file_name_to_upload = f"{file_id}-{filename}"
    resume_url = await upload_file_to_supabase(file_content, file_name_to_upload)

    # Create record in DB
    jd_record = await create_jd_match_record(_db_session, file_id, filename, resume_url)

    logger.info("ending upload_resume()")
    return ResumeUploadResponse(file_id=file_id, jd_match_id=jd_record.id)


async def process_jd(
    _db_session: Session,
    jd_match_id: str,
    jd_info: str,
) -> None:
    logger.info("starting process_jd()")
    # Update DB record with JD info
    await update_jd_info(_db_session, jd_match_id, jd_info)

    logger.info("ending process_jd()")


async def jd_match_init(
    jd_match_id: str,
    qstash: QStash | None = None,
    store: aioredis.Redis | None = None,
    _db_session: Session | None = None,
) -> JdMatchResponse:
    logger.info("starting jd_match_init for {jd_match_id}", jd_match_id=jd_match_id)

    if not store:
        raise ValueError("Redis store is not available")

    if not qstash:
        raise ValueError("QStash client is not available")

    if not _db_session:
        raise ValueError("Database session is not available")

    # Get record from DB
    jd_record = await get_jd_match_by_jd_match_id(_db_session, jd_match_id)
    if not jd_record:
        raise ValueError(f"No record found for file_id: {jd_match_id}")

    if not jd_record.jd:
        raise ValueError(f"JD info is missing for file_id: {jd_match_id}")

    target_url = f"{settings.API_URL}/jdmatch/{jd_match_id}/consumer"

    qstash.message.publish_json(url=target_url)

    await store.set(f"jdmatch:{jd_match_id}", JdMatchStatus.QUEUED.value)

    logger.info("ending jd_match_init()")

    return JdMatchResponse(file_id=jd_match_id)


async def jd_match_analyze(
    payload: ParseResumeJDInformation,
    store: aioredis.Redis | None = None,
    gemini_client: genai.Client | None = None,
    _db_session: Session | None = None,
    browser_use_client: AsyncBrowserUse | None = None,
) -> None:
    logger.info("starting jd_match_consumer()")

    if not store:
        raise ValueError("Redis store is not available")

    if not gemini_client:
        raise ValueError("Gemini client is not available")

    if not _db_session:
        raise ValueError("Database session is not available")

    file_name = payload.file_name
    file_id = file_name.split("-")[0]
    input_file_name = "-".join(file_name.split("-")[1:])
    jd_data = payload.jd_info
    candidate_resume_path = payload.candidate_resume_path

    try:
        is_jd_link = is_jd_link_or_description(jd_data)

        # Update status to EXTRACTING or ANALYZING
        status = (
            JdMatchStatus.EXTRACTING.value
            if is_jd_link
            else JdMatchStatus.ANALYZING.value
        )
        await store.set(f"jdmatch:{file_id}", status)

        # Extract or Analyze JD
        if is_jd_link:
            if not browser_use_client:
                raise ValueError(
                    "Browser use client is not available for link extraction"
                )
            jd = await agent_extract_jd(browser_use_client, jd_data)
        else:
            jd = agent_analyze_jd_text_structure(jd_data, gemini_client)

        # Update status to GENERATING
        await store.set(f"jdmatch:{file_id}", JdMatchStatus.THINKING.value)

        # Generate Candidate Score
        score_data_obj = agent_generate_candidate_score(
            jd, candidate_resume_path, gemini_client
        )
        score_data = score_data_obj.model_dump()

        # Save to Database
        await save_jd_match_info(
            _db_session,
            jd=jd,
            file_id=file_id,
            file_name=input_file_name,
            score_data=score_data,
        )

        # Update status to MATCHED and store final data
        result_data = {**score_data, "jd": jd}
        await store.set(f"jdmatch:{file_id}", JdMatchStatus.MATCHED.value)
        # We can also store the result data in Redis for fast retrieval if needed
        # In the TS version: await store.set(fileId, { status: JDMATCH_STATUS.MATCHED, data: { ...data, jd } });
        # Here we follow the pattern:
        await store.set(f"jdmatch:{file_id}:data", json.dumps(result_data))

        cleanup_file(candidate_resume_path)

    except Exception:
        logger.exception("Error in jd_match_consumer")
        await store.set(f"jdmatch:{file_id}", JdMatchStatus.FAILED.value)
        raise

    logger.info("ending jd_match_consumer()")
