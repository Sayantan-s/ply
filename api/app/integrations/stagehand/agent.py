from functools import lru_cache

from stagehand import AsyncStagehand

from app.core.config import settings


@lru_cache(maxsize=1)
def get_stagehand_client():
    return AsyncStagehand(server="local", local_chrome_path=settings.CHROME_PATH)
