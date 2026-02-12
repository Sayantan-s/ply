import asyncio
import json

from browser_use_sdk import BrowserUse

from app.core.config import settings
from app.core.logging.logger import get_logger
from app.integrations.llm.gemini import GeminiModel

logger = get_logger("extract_jd.agent")

_static_prompt = """
Strictly follow this json format output:

Success:
{
  "message": "SUCCESS",
  "data": "<Extracted Content Of the JD>"
}

Error:
{
  "message": "ERROR",
  "data": "<Error Message>"
}
"""


def _browsing_prompt(jd_url: str) -> str:
    return f"""
Navigate to the provided URL: {jd_url} and extract the Job Description (JD).

Rules:
> If any popup / modal / dialog is found on the screen, strictly close it!
> If you don't find the webpage as JD of job you can throw an error.
> Extract only the required job description, strictly donot extract unwanted things like about the company etc.

{_static_prompt}
"""


async def agent_extract_jd(jd_url: str) -> str:
    logger.info(f"Starting agent_extract_jd() for {jd_url}")

    client = BrowserUse(api_key=settings.BROWSER_USE_API_KEY)

    logger.info(f"Navigating to {jd_url}")

    task = client.tasks.create_task(
        task=_browsing_prompt(jd_url),
        llm=GeminiModel.pro,  # Default model
    )

    # Run the blocking task completion in a separate thread
    result = await asyncio.to_thread(task.complete)

    extracted = result.output

    if not extracted:
        raise ValueError("Agent produced no output")

    try:
        # Simple cleanup to handle potential markdown code blocks
        cleaned_output = extracted.strip()
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[7:]
        elif cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[3:]

        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[:-3]

        extracted_json = json.loads(cleaned_output.strip())
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from agent output: {extracted}")
        # Try to treat the whole output as data if JSON parsing fails, but respect the error protocol
        # If it failed to produce JSON, it might be a raw failure message or raw content.
        # Let's assume failure if not JSON, for safety, or wrap it.
        # But the prompt was strict.
        raise ValueError(f"Failed to parse agent output: {extracted}")

    jd_data = (
        extracted_json.get("data")
        if isinstance(extracted_json, dict)
        and extracted_json.get("message") == "SUCCESS"
        else None
    )

    if not jd_data:
        message = (
            extracted_json.get("data")
            if isinstance(extracted_json, dict)
            else "Unknown Error"
        )
        logger.error(f"Invalid response from agent: {message}")
        raise ValueError(message)

    logger.success(f"Extracted from {jd_url}")
    logger.info(f"Ending agent_extract_jd() for {jd_url}")

    return str(jd_data)
