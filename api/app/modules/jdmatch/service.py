import json

from fastapi import UploadFile
from google import genai
from qstash.client import QStash
from redis import asyncio as aioredis

from app.core.config import settings
from app.core.logging.logger import get_logger
from app.modules.jdmatch.agents.analyze_jd_text_structure import (
    agent_analyze_jd_text_structure,
)
from app.modules.jdmatch.agents.extract_jd import agent_extract_jd
from app.modules.jdmatch.agents.generate_candidate_score import (
    agent_generate_candidate_score,
)
from app.modules.jdmatch.constants import JdMatchStatus
from app.modules.jdmatch.repo import save_jd_match_info
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.modules.jdmatch.utils.cleanup_file import cleanup_file
from app.modules.jdmatch.utils.init_file import init_file
from app.modules.jdmatch.utils.init_file_identity import init_file_identity
from app.modules.jdmatch.utils.is_jd_link_or_description import (
    is_jd_link_or_description,
)
from app.modules.jdmatch.utils.save_file import save_file

# qstash_dependency removed since it's passed from API layer

logger = get_logger("jdmatch.service")


async def jd_match(
    resume_file: UploadFile | None = None,
    resume_url: str | None = None,
    jd_info: str | None = None,
    qstash: QStash | None = None,
    store: aioredis.Redis | None = None,
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
    payload: ParseResumeJDInformation,
    store: aioredis.Redis = None,
    gemini_client: genai.Client = None,
):
    logger.info("starting jd_match_consumer()")

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
            jd = await agent_extract_jd(jd_data)
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
