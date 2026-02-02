import json
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent

from app.core.config import settings
from app.core.logging.logger import get_logger
from app.integrations.browser_use.client import get_browser

logger = get_logger("extract_jd.agent")


async def agent_extract_jd(jd_url: str) -> str:
    logger.info(f"Starting agent_extract_jd() for {jd_url}")  # noqa: G004

    # specific model for browser use
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=settings.GEMINI_API_KEY,
    )

    browser = get_browser()

    task = f"""
    Navigate to the provided URL: {jd_url} and extract the Job Description (JD).

    Rules:
    > If any popup / modal / dialog is found on the screen, strictly close it!
    > If you don't find the webpage as JD of job you can throw an error.
    > Extract only the required job description, strictly do not extract unwanted things like about the company etc.

    Return the result in the following JSON format:
    {{
      "message": "SUCCESS",
      "data": "<Extracted Content Of the JD>"
    }}
    Or if error:
    {{
      "message": "ERROR",
      "data": "<Error Message>"
    }}
    """

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
    )

    logger.info(f"Navigating to {jd_url} with browser-use agent")  # noqa: G004

    history = await agent.run()

    # Extract result
    result = history.final_result()
    if not result:
        logger.error("Agent returned no result")
        raise ValueError("Agent returned no result")

    try:
        # Cleanup code blocks
        cleaned_result = result.strip()
        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result[7:]
        elif cleaned_result.startswith("```"):
            cleaned_result = cleaned_result[3:]

        if cleaned_result.endswith("```"):
            cleaned_result = cleaned_result[:-3]

        cleaned_result = cleaned_result.strip()

        extracted = json.loads(cleaned_result)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse JSON from agent result: {result[:100]}...")  # noqa: G004
        # Attempt to construct success if it looks like content
        extracted = {"message": "SUCCESS", "data": result}

    jd_data = (
        extracted.get("data")
        if isinstance(extracted, dict) and extracted.get("message") == "SUCCESS"
        else None
    )

    if not jd_data:
        message = (
            extracted.get("data") if isinstance(extracted, dict) else "Unknown Error"
        )
        logger.error(f"Invalid response from agent: {message}")  # noqa: G004
        raise ValueError(message)

    logger.success(f"Extracted from {jd_url}")  # noqa: G004
    logger.info(f"Ending agent_extract_jd() for {jd_url}")  # noqa: G004

    return str(jd_data)
