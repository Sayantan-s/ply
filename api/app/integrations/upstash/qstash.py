from functools import lru_cache
from typing import Generator
from qstash.client import QStash
from qstash.receiver import Receiver
from app.core.config import settings

@lru_cache()
def _get_client() -> QStash:
    return QStash(settings.QSTASH_TOKEN)

def get_qstash_client() -> Generator[QStash, None, None]:
    """
    Dependency to get QStash client.
    """
    client = _get_client()
    yield client

@lru_cache()
def _get_consumer() -> Receiver:
    return Receiver(
         current_signing_key=settings.QSTASH_CURRENT_SIGNING_KEY,
         next_signing_key=settings.QSTASH_NEXT_SIGNING_KEY,
    )

def get_qstash_consumer() -> Generator[Receiver, None, None]:
    """
    Dependency to get QStash consumer.
    """
    client = _get_consumer()
    yield client