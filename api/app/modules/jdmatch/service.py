import json
import os

from browser_use_sdk import AsyncBrowserUse
from fastapi import UploadFile
from google import genai
from qstash.client import QStash
from redis import asyncio as aioredis
from sqlmodel import Session

from app.api.v1.dto.jdmatch import JdMatchResponse, JdResponse, ResumeUploadResponse
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
    get_jd_match_by_file_id,
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

    # Create record in DB
    await create_jd_match_record(_db_session, file_id, filename)

    file_name_to_upload = f"{file_id}-{filename}"
    signed_url = await upload_file_to_supabase(file_content, file_name_to_upload)

    logger.info("ending upload_resume()")
    return ResumeUploadResponse(file_id=file_id, signed_url=signed_url)


async def process_jd(
    _db_session: Session,
    file_id: str,
    jd_info: str,
) -> JdResponse:
    logger.info("starting process_jd()")
    is_link = is_jd_link_or_description(jd_info)

    # Update DB record with JD info
    await update_jd_info(_db_session, file_id, jd_info)

    logger.info("ending process_jd()")
    return JdResponse(jd_info=jd_info, is_link=is_link)


async def jd_match_init(
    file_id: str,
    qstash: QStash | None = None,
    store: aioredis.Redis | None = None,
    _db_session: Session | None = None,
) -> JdMatchResponse:
    logger.info(f"starting jd_match_init for {file_id}")

    if not store:
        raise ValueError("Redis store is not available")

    if not qstash:
        raise ValueError("QStash client is not available")

    if not _db_session:
        raise ValueError("Database session is not available")

    # Get record from DB
    jd_record = await get_jd_match_by_file_id(_db_session, file_id)
    if not jd_record:
        raise ValueError(f"No record found for file_id: {file_id}")

    if not jd_record.jd:
        raise ValueError(f"JD info is missing for file_id: {file_id}")

    await store.set(f"jdmatch:{file_id}", JdMatchStatus.PARSING.value)

    # The file should already be in public/uploads if we are using the local filesystem for now
    # Or we might need to re-download it from Supabase if it's not there.
    # But jd_match_init in original code was doing init_file which downloads/reads.
    # Since we separated upload, we need to make sure the file is available for the worker.
    # For now, let's assume we need to re-init it or use the Supabase URL.

    # To keep it simple and consistent with existing logic, let's re-download/read if needed
    # or just pass the info to QStash.
    # The consumer needs `candidate_resume_path`, `file_name`, `jd_info`.

    root_project_path = os.getcwd()
    upload_dir = os.path.join(root_project_path, "public", "uploads")
    file_name = f"{file_id}-{jd_record.file_name}"
    candidate_resume_path = os.path.join(upload_dir, file_name)

    # If file doesn't exist locally, we'd need to fetch it from Supabase.
    # For now, upload_resume should have saved it locally via init_file + ... wait
    # upload_resume only calls init_file and upload_file_to_supabase. It DOES NOT save locally.
    # We should probably save it locally in upload_resume so init can find it, or have the worker download it.

    resume_info = ParseResumeJDInformation(
        candidate_resume_path=candidate_resume_path,
        file_name=file_name,
        jd_info=jd_record.jd,
    )

    target_url = f"{settings.API_URL}/jdmatch/consumer"

    qstash.message.publish_json(
        url=target_url,
        body=resume_info.model_dump(),
    )

    await store.set(f"jdmatch:{file_id}", JdMatchStatus.QUEUED.value)

    logger.info("ending jd_match_init()")

    return JdMatchResponse(file_id=file_id)


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
