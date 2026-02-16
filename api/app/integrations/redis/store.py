from functools import lru_cache

from redis import asyncio as aioredis

from app.core.config import settings
from app.core.logging.logger import get_logger

logger = get_logger("redis.store")

redis_client: aioredis.Redis = aioredis.from_url(
    settings.get_redis_url(), decode_responses=True
)


async def connect_to_redis() -> None:
    logger.info("Starting Redis initialization...")
    await redis_client.ping()
    logger.success(
        "Redis initialization completed", extra={"redis_client": redis_client}
    )


@lru_cache(maxsize=1)
def get_redis_store() -> aioredis.Redis:
    """Dependency to inject Redis client into routes/services"""
    return redis_client
