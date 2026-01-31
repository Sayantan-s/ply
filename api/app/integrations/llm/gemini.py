from dataclasses import dataclass
from functools import lru_cache

from google import genai

from app.core.config import settings

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
_gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)


@lru_cache(maxsize=1)
def get_gemini_client() -> genai.Client:
    return _gemini_client


@dataclass(frozen=True)
class GeminiModel:
    flash = "gemini-flash-lite-latest"
    flash_preview = "gemini-3-flash-preview"
    pro = "gemini-3-pro-preview"
