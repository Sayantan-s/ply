from browser_use_sdk import AsyncBrowserUse

from app.core.config import settings


def get_browser_use_client() -> AsyncBrowserUse:
    return AsyncBrowserUse(api_key=settings.BROWSER_USE_API_KEY)
