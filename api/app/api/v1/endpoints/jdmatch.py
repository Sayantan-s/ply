from typing import Annotated

from browser_use_sdk import AsyncBrowserUse
from fastapi import APIRouter, Depends, Form, Path, UploadFile, status
from fastapi.responses import StreamingResponse
from google import genai
from sqlmodel import Session

from app.api.v1.dto import ResponseEnvelope
from app.api.v1.dto.jdmatch import (
    JdMatchStatusResponse,
    ResumeUploadResponse,
)
from app.core.logging.logger import get_logger
from app.integrations.browser_use.agent import get_browser_use_client
from app.integrations.db.database import get_session
from app.integrations.llm.gemini import get_gemini_client
from app.modules.jdmatch.service import (
    create_jd_match,
    get_jd_match_status,
    jd_match_analyze,
)

router: APIRouter = APIRouter()

logger = get_logger("jdmatch.api")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEnvelope[ResumeUploadResponse],
    operation_id="createJdMatch",
)
async def create_jd_match_endpoint(
    session: Annotated[Session, Depends(get_session)],
    resume_file: UploadFile | None = None,
    resume_url: Annotated[str | None, Form()] = None,
    jd_info: Annotated[str | None, Form()] = None,
) -> ResponseEnvelope[ResumeUploadResponse]:
    logger.info("starting create_jd_match_endpoint()")
    response = await create_jd_match(session, resume_file, resume_url, jd_info)
    logger.info("ending create_jd_match_endpoint()")
    return ResponseEnvelope.ok(response)


@router.post(
    "/{jd_match_id}/analyze",
    status_code=status.HTTP_200_OK,
    operation_id="analyzeJdMatch",
)
async def analyze_jd_match_endpoint(
    jd_match_id: Annotated[str, Path(...)],
    gemini_client: Annotated[genai.Client, Depends(get_gemini_client)],
    session: Annotated[Session, Depends(get_session)],
    browser_use_client: Annotated[AsyncBrowserUse, Depends(get_browser_use_client)],
) -> StreamingResponse:
    logger.info(
        "starting analyze_jd_match_endpoint for {jd_match_id}", jd_match_id=jd_match_id
    )

    async def event_generator():
        async for chunk in jd_match_analyze(
            jd_match_id, gemini_client, session, browser_use_client
        ):
            yield chunk.model_dump_json() + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@router.get(
    "/{jd_match_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEnvelope[JdMatchStatusResponse],
    operation_id="getJdMatchStatus",
)
async def get_jd_match_status_endpoint(
    jd_match_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> ResponseEnvelope[JdMatchStatusResponse]:
    logger.info(
        "starting get_jd_match_status_endpoint for {jd_match_id}",
        jd_match_id=jd_match_id,
    )
    response = await get_jd_match_status(jd_match_id, session)
    logger.info(
        "ending get_jd_match_status_endpoint for {jd_match_id}", jd_match_id=jd_match_id
    )
    return ResponseEnvelope.ok(response)
