from collections.abc import AsyncGenerator, Generator

from google import genai
from google.genai import types

from app.core.logging.logger import get_logger
from app.integrations.llm.gemini import GeminiModel
from app.modules.jdmatch.schemas import (
    AgentResponseCandidateScore,
    AgentResponseStructuredScore,
)

logger = get_logger("generate_candidate_score.agent")


_ai_so_type = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["score", "matching_skills", "missing_skills", "explanation"],
    properties={
        "score": genai.types.Schema(
            type=genai.types.Type.INTEGER,
        ),
        "matching_skills": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING),
        ),
        "missing_skills": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING),
        ),
        "explanation": genai.types.Schema(
            type=genai.types.Type.STRING,
        ),
    },
)

_safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]


def _prompt(jd: str) -> str:
    return f"""
      You are an ATS machine that judges candidates based on JDs provided to you.
      Below is the JD of the job.

      {jd}

      Do these following tasks taking reference from the above JD and file input:

      > Analyze the candidate resume given as an input
      > Check if the candidate is fit for the job or not.
      > Rate the candidate based on the below structure.

      Note: assess the score logic in this manner -> score < 40 = POOR, score > 40 && score < 70 = AVERAGE, score > 70 && score < 90 = GOOD, score > 90 = GREAT

      IMPORTANT: YOUR RESPONSE MUST BE A VALID JSON OBJECT MATCHING THE SCHEMA.
      DO NOT INCLUDE ANY MARKDOWN FORMATTING (like ```json).
    """


def agent_generate_candidate_score(
    jd: str, resume_path: str, gemini_client: genai.Client | None = None
) -> AgentResponseCandidateScore:
    if not gemini_client:
        raise ValueError("Gemini client is not available")

    # Upload file to Gemini
    file = gemini_client.files.upload(file=resume_path)

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=_ai_so_type,
        safety_settings=_safety_settings,
    )

    response = gemini_client.models.generate_content(
        model=GeminiModel.flash,
        contents=[file, _prompt(jd)],
        config=generate_content_config,
    )

    # Clean up uploaded file from Gemini (optional but recommended)
    gemini_client.files.delete(name=file.name)

    _llm_response = response.text
    _candidate_score = AgentResponseCandidateScore.model_validate_json(_llm_response)
    logger.success("Response from Gemini: %s", _candidate_score)
    return _candidate_score


async def agent_stream_candidate_score(
    jd: str, resume_path: str, gemini_client: genai.Client | None = None
) -> AsyncGenerator[str, None]:
    if not gemini_client:
        raise ValueError("Gemini client is not available")

    # Upload file to Gemini
    file = gemini_client.files.upload(file=resume_path)

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=_ai_so_type,
        safety_settings=_safety_settings,
    )

    stream = gemini_client.models.generate_content_stream(
        model=GeminiModel.flash,
        contents=[file, _prompt(jd)],
        config=generate_content_config,
    )

    for chunk in stream:
        if chunk.text:
            logger.info("Chunk from Gemini: %s", chunk.text)
            yield chunk.text

    # Clean up uploaded file from Gemini
    gemini_client.files.delete(name=file.name)


_ai_structured_score_type = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=["score", "matching_skills", "missing_skills"],
    properties={
        "score": genai.types.Schema(type=genai.types.Type.INTEGER),
        "matching_skills": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING),
        ),
        "missing_skills": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(type=genai.types.Type.STRING),
        ),
    },
)


def _structured_prompt(jd: str) -> str:
    return f"""
      You are an ATS machine that judges candidates based on JDs provided to you.
      Below is the JD of the job.

      {jd}

      Do these following tasks taking reference from the above JD and file input:

      > Analyze the candidate resume given as an input
      > Check if the candidate is fit for the job or not.
      > Rate the candidate based on the below structure.

      Note: assess the score logic in this manner -> score < 40 = POOR, score > 40 && score < 70 = AVERAGE, score > 70 && score < 90 = GOOD, score > 90 = GREAT

      Return ONLY the score, matching_skills, and missing_skills as a JSON object.
      DO NOT include an explanation field.
      IMPORTANT: YOUR RESPONSE MUST BE A VALID JSON OBJECT MATCHING THE SCHEMA.
      DO NOT INCLUDE ANY MARKDOWN FORMATTING (like ```json).
    """


def _explanation_prompt(
    jd: str, score: int, matching_skills: list[str], missing_skills: list[str]
) -> str:
    return f"""
      You are an ATS machine that judges candidates based on JDs provided to you.
      Below is the JD of the job.

      {jd}

      You have already scored this candidate's resume:
      - Score: {score}
      - Matching Skills: {", ".join(matching_skills)}
      - Missing Skills: {", ".join(missing_skills)}

      Now write a detailed explanation of why the candidate received this score.
      Cover their strengths, weaknesses, and areas for improvement relative to the JD.
      Write in plain text paragraphs, NOT JSON.
    """


def agent_generate_structured_score(
    jd: str, resume_path: str, gemini_client: genai.Client | None = None
) -> AgentResponseStructuredScore:
    if not gemini_client:
        raise ValueError("Gemini client is not available")

    file = gemini_client.files.upload(file=resume_path)

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=_ai_structured_score_type,
        safety_settings=_safety_settings,
    )

    response = gemini_client.models.generate_content(
        model=GeminiModel.flash,
        contents=[file, _structured_prompt(jd)],
        config=generate_content_config,
    )

    _llm_response = response.text
    result = AgentResponseStructuredScore.model_validate_json(_llm_response)
    logger.success("Structured score from Gemini: %s", result)

    # Keep the uploaded file for explanation streaming (caller cleans up)
    gemini_client.files.delete(name=file.name)

    return result


def agent_stream_explanation(
    jd: str,
    resume_path: str,
    structured_result: AgentResponseStructuredScore,
    gemini_client: genai.Client | None = None,
) -> Generator[str, None, None]:
    if not gemini_client:
        raise ValueError("Gemini client is not available")

    file = gemini_client.files.upload(file=resume_path)

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        safety_settings=_safety_settings,
    )

    prompt = _explanation_prompt(
        jd,
        structured_result.score,
        structured_result.matching_skills,
        structured_result.missing_skills,
    )

    stream = gemini_client.models.generate_content_stream(
        model=GeminiModel.flash,
        contents=[file, prompt],
        config=generate_content_config,
    )

    for chunk in stream:
        if chunk.text:
            logger.info("Explanation chunk from Gemini: %s", chunk.text)
            yield chunk.text

    gemini_client.files.delete(name=file.name)
