from functools import lru_cache
from typing import Generator
from qstash.client import QStash

@lru_cache()
def _get_client() -> QStash:
    return QStash.from_env()

def get_qstash_client() -> Generator[QStash, None, None]:
    """
    Dependency to get QStash client.
    """
    client = _get_client()
    yield client