from google import genai
from google.genai import types

from app.integrations.llm.gemini import GeminiModel
from app.modules.jdmatch.schemas import AgentResponseCandidateScore

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


def _prompt(jd: str):
    return f"""
      You are an ATS machine that judges candidates based on JDs provided to you.
      Below is the JD of the job.

      {jd}

      Do these following tasks taking reference from the above JD and file input:

      > Analyze the candidate resume given as an input
      > Check if the candidate is fit for the job or not.
      > Rate the candidate based on the below structure.

      Note: assess the score logic in this manner -> score < 40 = POOR, score > 40 && score < 70 = AVERAGE, score > 70 && score < 90 = GOOD, score > 90 = GREAT
    """


def agent_generate_candidate_score(
    jd: str, resume_path: str, gemini_client: genai.Client = None
) -> AgentResponseCandidateScore:
    # Upload file to Gemini
    file = gemini_client.files.upload(path=resume_path)

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1,
        ),
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

    data = response.json()
    return AgentResponseCandidateScore(**data)
