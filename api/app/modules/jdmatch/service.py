from typing import AsyncGenerator

from browser_use_sdk import AsyncBrowserUse
from fastapi import UploadFile
from google import genai
from sqlmodel import Session

from app.api.v1.dto.jdmatch import (
    AnalysisStreamResponse,
    JdMatchStreamResponse,
    JdMatchStatusResponse,
    ResumeUploadResponse,
    StatusStreamResponse,
)
from app.core.logging.logger import get_logger
from app.integrations.supabase.storage import upload_file_to_supabase
from app.modules.jdmatch.agents.analyze_jd_text_structure import (
    agent_analyze_jd_text_structure,
)
from app.modules.jdmatch.agents.extract_jd import agent_extract_jd
from app.modules.jdmatch.agents.generate_candidate_score import (
    agent_stream_candidate_score,
)
from app.modules.jdmatch.constants import JdMatchStatus
from app.modules.jdmatch.repo import (
    create_jd_match_record,
    get_jd_match_by_jd_match_id,
    save_jd_match_info,
    update_jd_match_status,
)
from app.modules.jdmatch.utils.cleanup_file import cleanup_file
from app.modules.jdmatch.utils.download_resume import download_resume
from app.modules.jdmatch.utils.init_file import init_file
from app.modules.jdmatch.utils.init_file_identity import init_file_identity
from app.modules.jdmatch.utils.is_jd_link_or_description import (
    is_jd_link_or_description,
)
from app.modules.jdmatch.utils.save_file import save_file

logger = get_logger("jdmatch.service")


async def create_jd_match(
    _db_session: Session,
    resume_file: UploadFile | None = None,
    resume_url: str | None = None,
    jd_info: str | None = None,
) -> ResumeUploadResponse:
    logger.info("starting create_jd_match()")

    file_id = init_file_identity(resume_url or "")
    file_content, filename, file_id = await init_file(
        resume_file, resume_url, file_id=file_id
    )

    # Upload file to Storage
    file_name_to_upload = f"{file_id}-{filename}"
    resume_url = await upload_file_to_supabase(file_content, file_name_to_upload)

    # Create record in DB
    jd_record = await create_jd_match_record(
        _db_session, file_id, filename, resume_url, jd_info
    )

    logger.info("ending create_jd_match()")
    return ResumeUploadResponse(file_id=file_id, jd_match_id=jd_record.id)


async def jd_match_analyze(
    jd_match_id: str,
    gemini_client: genai.Client,
    _db_session: Session,
    browser_use_client: AsyncBrowserUse | None = None,
) -> AsyncGenerator[JdMatchStreamResponse, None]:
    logger.info("starting jd_match_analyze()")

    # Fetch jd_match record
    jd_record = await get_jd_match_by_jd_match_id(_db_session, jd_match_id)
    if not jd_record:
        raise ValueError(f"No record found for jd_match_id: {jd_match_id}")

    jd_data = jd_record.jd
    if not jd_data:
        raise ValueError(f"JD info is missing for jd_match_id: {jd_match_id}")

    # Download resume locally
    file_content, filename, file_id = await download_resume(jd_record.resume_url)

    # Save file locally to get path for agent
    parse_info = save_file(file_content, jd_data, filename, file_id)
    candidate_resume_path = parse_info.candidate_resume_path

    try:
        is_jd_link = is_jd_link_or_description(jd_data)

        # Update status to EXTRACTING or ANALYZING in DB
        status = (
            JdMatchStatus.EXTRACTING
            if is_jd_link
            else JdMatchStatus.ANALYZING
        )
        await update_jd_match_status(_db_session, jd_match_id, status.value)
        yield JdMatchStreamResponse(payload=StatusStreamResponse(status=status))

        # Extract or Analyze JD
        if is_jd_link:
            if not browser_use_client:
                raise ValueError(
                    "Browser use client is not available for link extraction"
                )
            jd = await agent_extract_jd(browser_use_client, jd_data)
        else:
            jd = agent_analyze_jd_text_structure(jd_data, gemini_client)

        # Update status to THINKING in DB
        await update_jd_match_status(
            _db_session, jd_match_id, JdMatchStatus.THINKING.value
        )
        yield JdMatchStreamResponse(
            payload=StatusStreamResponse(status=JdMatchStatus.THINKING)
        )

        # Generate Candidate Score (Streaming)
        full_analysis_text = ""
        async for chunk in agent_stream_candidate_score(
            jd, candidate_resume_path, gemini_client
        ):
            full_analysis_text += chunk
            yield JdMatchStreamResponse(payload=AnalysisStreamResponse(chunk=chunk))

        # Parse the final aggregated text to JSON
        try:
            from app.modules.jdmatch.schemas import AgentResponseCandidateScore

            score_data = AgentResponseCandidateScore.model_validate_json(
                full_analysis_text
            ).model_dump()
        except Exception as e:
            logger.error(f"Failed to parse analysis JSON: {e}")
            raise

        # Save to Database (this will also update status to MATCHED)
        await save_jd_match_info(
            _db_session,
            jd_match_id=jd_match_id,
            jd=jd,
            score_data=score_data,
        )
        yield JdMatchStreamResponse(
            payload=StatusStreamResponse(status=JdMatchStatus.MATCHED)
        )

        cleanup_file(candidate_resume_path)

    except Exception:
        logger.exception("Error in jd_match_analyze")
        await update_jd_match_status(
            _db_session, jd_match_id, JdMatchStatus.FAILED.value
        )
        yield JdMatchStreamResponse(
            payload=StatusStreamResponse(status=JdMatchStatus.FAILED)
        )
        raise

    logger.info("ending jd_match_analyze()")


async def get_jd_match_status(
    jd_match_id: str,
    _db_session: Session,
) -> JdMatchStatusResponse:
    logger.info("getting status for {jd_match_id}", jd_match_id=jd_match_id)

    jd_record = await get_jd_match_by_jd_match_id(_db_session, jd_match_id)
    if not jd_record:
        raise ValueError(f"No record found for jd_match_id: {jd_match_id}")

    return JdMatchStatusResponse(status=jd_record.status)
