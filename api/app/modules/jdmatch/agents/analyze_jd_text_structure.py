from google import genai
from google.genai import types

from app.integrations.llm.gemini import GeminiModel
from app.modules.jdmatch.schemas import AgentResponseJDVerification

_ai_so_type = (
    genai.types.Schema(
        type=genai.types.Type.OBJECT,
        required=["is_jd", "reason"],
        properties={
            "is_jd": genai.types.Schema(
                type=genai.types.Type.BOOLEAN,
            ),
            "reason": genai.types.Schema(
                type=genai.types.Type.STRING,
            ),
        },
    ),
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


def _prompt(text: str):
    return f"""
      You are recruiter who can understand the JD of a job.
      You are given a text structure from which you have to understand that it's a JD or not.
      Please analyze the text and respond in the below JSON format.

      Text Structure:
      {text}

      Response Format:

      {{
        "is_jd": true,
        "reason": ""
      }}

      OR

      {{
        "is_jd": false,
        "reason": "<Reason why it's not a JD>"
      }}
    """


def agent_analyze_jd_text_structure(
    text: str, gemini_client: genai.Client = None
) -> str:
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=_prompt(text)),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=2500,
        ),
        response_mime_type="application/json",
        response_schema=_ai_so_type,
        safety_settings=_safety_settings,
    )

    response = gemini_client.models.generate_content(
        model=GeminiModel.flash,
        contents=contents,
        config=generate_content_config,
    )

    data = response.json()
    agent_response = AgentResponseJDVerification(**data)

    if not agent_response.is_jd:
        raise ValueError(agent_response.reason)

    return text
