from functools import lru_cache

from stagehand import AsyncStagehand


@lru_cache(maxsize=1)
def get_stagehand_client():
    return AsyncStagehand()
