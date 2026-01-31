from stagehand import AsyncStagehand

from app.core.logging.logger import get_logger
from app.integrations.llm.gemini import GeminiModel

_BROWSING_PROMPT = """
      You are smart machine that understands and extracts contents from webpages.
      Below content should be a JD of a certain job.
      As I mentioned "Should", there can be posibility that you might a find a different webpage which might not be a JD page of example it can be a login page, a shopping card.

      Rules:

      > If you don't find the webpage as JD of job you can throw an error.
      > Extract only the required job description, strictly donot extract unwanted things like about the company etc.

      Strictly follow this json format output::

      Success:

      {
        message: 'SUCCESS',
        data: "<Extracted Content Of the JD>" // for e.g. This is a key role within the Global Deal Desk team, which owns deal strategy, quote-to-cash execution, and pricing operations. You’ll work closely with sales, product, legal, and operations teams to ensure that CPQ changes reflect business prior....
      }

      Error:

      {
        message: 'ERROR',
        data: "<Error Message>" // add error reason in this data property like -> UNKNOWN PAGE, DIFFICULT TO REACH, BLOCKERS CAME UP etc
      }
"""

_ACTION_PROMPT = (
    "If any popup / modal / dialog is found on the screen, strictly close it!"
)

_TIMEOUT = 60000

logger = get_logger("extract_jd.agent")


async def agent_extract_jd(jd_url: str, stagehand_client: AsyncStagehand):
    logger.info(f"Starting agent_extract_jd() for {jd_url}")
    session = await stagehand_client.sessions.start(model_name=GeminiModel.pro)
    logger.info(f"Navigating to {jd_url}")
    await session.navigate(url=jd_url)
    logger.success(f"Navigated to {jd_url}")

    await session.act(_ACTION_PROMPT)
    logger.success(f"Acted on {jd_url}")

    extract_response = await session.extract(
        instruction=_BROWSING_PROMPT,
        schema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "data": {"type": "string"},
            },
            "required": ["message", "data"],
        },
    )

    extracted = extract_response.data.result
    jd_data = (
        extracted.get("data")
        if isinstance(extracted, dict) and extracted.get("message") == "SUCCESS"
        else None
    )

    if not jd_data:
        message = extracted.get("data") if isinstance(extracted, dict) else None
        logger.error(f"Invalid response from agent: {message}")
        raise ValueError(message)

    logger.success(f"Extracted from {jd_url}")

    await session.end()
    logger.info(f"Ending agent_extract_jd() for {jd_url}")

    return jd_data
