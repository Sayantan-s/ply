from redis import asyncio as aioredis
from app.core.config import settings

redis_client: aioredis.Redis = aioredis.from_url(
    settings.get_redis_url(), decode_responses=True
)


def get_redis_store() -> aioredis.Redis:
    """Dependency to inject Redis client into routes/services"""
    return redis_client
