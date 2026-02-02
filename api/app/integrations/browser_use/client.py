from functools import lru_cache

from browser_use import Browser


@lru_cache(maxsize=1)
def get_browser() -> Browser:
    return Browser(
        cdp_url="ws://localhost:3002",
    )
