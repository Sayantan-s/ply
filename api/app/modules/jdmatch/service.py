from collections.abc import AsyncGenerator

from browser_use_sdk import AsyncBrowserUse
from fastapi import UploadFile
from google import genai
from sqlmodel import Session

from app.api.v1.dto.jdmatch import (
    AnalysisDeltaEvent,
    AnalysisStartEvent,
    AnalysisStopEvent,
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    ContentBlockStopEvent,
    ErrorEvent,
    ExplanationContentBlock,
    JdMatchAnalysisResponse,
    JdMatchStatusResponse,
    ResultContentBlock,
    ResultDelta,
    ResumeUploadResponse,
    SSEEvent,
    SSEEventType,
    StatusUpdateEvent,
    StopReason,
    TextDelta,
)
from app.core.logging.logger import get_logger
from app.integrations.supabase.storage import upload_file_to_supabase
from app.modules.jdmatch.agents.analyze_jd_text_structure import (
    agent_analyze_jd_text_structure,
)
from app.modules.jdmatch.agents.extract_jd import agent_extract_jd
from app.modules.jdmatch.agents.generate_candidate_score import (
    agent_generate_structured_score,
    agent_stream_explanation,
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
) -> AsyncGenerator[tuple[SSEEventType, SSEEvent], None]:
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
    parse_info = save_file(file_content, jd_data, filename, file_id, jd_match_id)
    candidate_resume_path = parse_info.candidate_resume_path

    try:
        # analysis_start
        yield (
            SSEEventType.ANALYSIS_START,
            AnalysisStartEvent(analysis_id=jd_match_id),
        )

        is_jd_link = is_jd_link_or_description(jd_data)

        # Update status to EXTRACTING or ANALYZING in DB
        status = JdMatchStatus.EXTRACTING if is_jd_link else JdMatchStatus.ANALYZING
        await update_jd_match_status(_db_session, jd_match_id, status.value)
        yield (SSEEventType.STATUS_UPDATE, StatusUpdateEvent(status=status))

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
        yield (
            SSEEventType.STATUS_UPDATE,
            StatusUpdateEvent(status=JdMatchStatus.THINKING),
        )

        # Phase 1: Generate structured score (non-streaming)
        structured_result = agent_generate_structured_score(
            jd, candidate_resume_path, gemini_client
        )

        # Content block 0: result
        yield (
            SSEEventType.CONTENT_BLOCK_START,
            ContentBlockStartEvent(index=0, content_block=ResultContentBlock()),
        )
        yield (
            SSEEventType.CONTENT_BLOCK_DELTA,
            ContentBlockDeltaEvent(
                index=0,
                delta=ResultDelta(
                    score=structured_result.score,
                    matching_skills=structured_result.matching_skills,
                    missing_skills=structured_result.missing_skills,
                ),
            ),
        )
        yield (SSEEventType.CONTENT_BLOCK_STOP, ContentBlockStopEvent(index=0))

        # Content block 1: explanation (streamed)
        yield (
            SSEEventType.CONTENT_BLOCK_START,
            ContentBlockStartEvent(
                index=1, content_block=ExplanationContentBlock()
            ),
        )

        # Phase 2: Stream explanation text
        full_explanation = ""
        for chunk in agent_stream_explanation(
            jd, candidate_resume_path, structured_result, gemini_client
        ):
            full_explanation += chunk
            yield (
                SSEEventType.CONTENT_BLOCK_DELTA,
                ContentBlockDeltaEvent(index=1, delta=TextDelta(text=chunk)),
            )

        yield (SSEEventType.CONTENT_BLOCK_STOP, ContentBlockStopEvent(index=1))

        # Build score_data for DB save
        score_data = {
            "score": structured_result.score,
            "matching_skills": structured_result.matching_skills,
            "missing_skills": structured_result.missing_skills,
            "explanation": full_explanation,
        }

        # Save to Database (this will also update status to MATCHED)
        await save_jd_match_info(
            _db_session,
            jd_match_id=jd_match_id,
            jd=jd,
            score_data=score_data,
        )
        yield (
            SSEEventType.STATUS_UPDATE,
            StatusUpdateEvent(status=JdMatchStatus.MATCHED),
        )

        cleanup_file(candidate_resume_path)

        # analysis_delta + analysis_stop
        yield (
            SSEEventType.ANALYSIS_DELTA,
            AnalysisDeltaEvent(stop_reason=StopReason.COMPLETE),
        )
        yield (SSEEventType.ANALYSIS_STOP, AnalysisStopEvent())

    except Exception:
        logger.exception("Error in jd_match_analyze")
        await update_jd_match_status(
            _db_session, jd_match_id, JdMatchStatus.FAILED.value
        )
        yield (
            SSEEventType.ERROR,
            ErrorEvent(message="Analysis failed"),
        )
        yield (
            SSEEventType.ANALYSIS_DELTA,
            AnalysisDeltaEvent(stop_reason=StopReason.ERROR),
        )
        yield (SSEEventType.ANALYSIS_STOP, AnalysisStopEvent())
        return

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


async def get_jd_match_analysis(
    jd_match_id: str,
    _db_session: Session,
) -> JdMatchAnalysisResponse:
    logger.info("getting analysis for {jd_match_id}", jd_match_id=jd_match_id)

    jd_record = await get_jd_match_by_jd_match_id(_db_session, jd_match_id)
    if not jd_record:
        raise ValueError(f"No record found for jd_match_id: {jd_match_id}")

    return JdMatchAnalysisResponse(
        jd_match_id=jd_record.id,
        status=jd_record.status,
        score=jd_record.score,
        matching_skills=jd_record.matching_skills,
        missing_skills=jd_record.missing_skills,
        explanation=jd_record.explanation,
    )
