from google import genai
from google.genai import types

from app.core.logging.logger import get_logger
from app.integrations.llm.gemini import GeminiModel

logger = get_logger("extract_jd.agent")

_static_prompt = """
Strictly follow this json format output:

Success:
{
  message: 'SUCCESS',
  data: "<Extracted Content Of the JD>"
}

Error:
{
  message: 'ERROR',
  data: "<Error Message>"
}
"""


def _browsing_prompt(jd_url: str) -> str:
    return f"""
You are a smart machine that understands and extracts contents from webpages.
Navigate to the provided URL: {jd_url} and extract the Job Description (JD).

Rules:
> If any popup / modal / dialog is found on the screen, strictly close it!
> If you don't find the webpage as JD of job you can throw an error.
> Extract only the required job description, strictly donot extract unwanted things like about the company etc.

{_static_prompt}
"""


_so_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "message": types.Schema(type=types.Type.STRING),
        "data": types.Schema(type=types.Type.STRING),
    },
    required=["message", "data"],
)


async def agent_extract_jd(jd_url: str, gemini_client: genai.Client):
    logger.info(f"Starting agent_extract_jd() for {jd_url}")

    generate_content_config = types.GenerateContentConfig(
        tools=[
            types.Tool(
                computer_use=types.ComputerUse(
                    environment=types.Environment.ENVIRONMENT_BROWSER,
                )
            ),
        ],
        response_mime_type="application/json",
        response_schema=_so_schema,
    )

    logger.info(f"Navigating to {jd_url}")

    # Using the specific model for computer use
    response = gemini_client.models.generate_content(
        model=GeminiModel.computer_use,
        contents=_browsing_prompt(jd_url),
        config=generate_content_config,
    )

    extracted = response.json()

    jd_data = (
        extracted.get("data")
        if isinstance(extracted, dict) and extracted.get("message") == "SUCCESS"
        else None
    )

    if not jd_data:
        message = (
            extracted.get("data") if isinstance(extracted, dict) else "Unknown Error"
        )
        logger.error(f"Invalid response from agent: {message}")
        raise ValueError(message)

    logger.success(f"Extracted from {jd_url}")
    logger.info(f"Ending agent_extract_jd() for {jd_url}")

    return jd_data
