from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.integrations.browser_use.agent import get_browser_use_client
from app.integrations.db.database import get_session
from app.integrations.llm.gemini import get_gemini_client
from app.integrations.redis.store import get_redis_store
from app.integrations.upstash.qstash import get_qstash_client, get_qstash_consumer
from app.main import app


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_redis():
    return AsyncMock()


@pytest.fixture
def mock_qstash():
    return MagicMock()


@pytest.fixture
def mock_receiver():
    return MagicMock()


@pytest.fixture
def mock_gemini():
    return MagicMock()


@pytest.fixture
def mock_browser_use():
    return AsyncMock()


@pytest.fixture
async def client(
    mock_session, mock_redis, mock_qstash, mock_receiver, mock_gemini, mock_browser_use
):
    def _get_session_override():
        yield mock_session

    def _get_redis_override():
        return mock_redis

    def _get_qstash_client_override():
        yield mock_qstash

    def _get_qstash_consumer_override():
        yield mock_receiver

    def _get_gemini_client_override():
        return mock_gemini

    def _get_browser_use_client_override():
        return mock_browser_use

    app.dependency_overrides[get_session] = _get_session_override
    app.dependency_overrides[get_redis_store] = _get_redis_override
    app.dependency_overrides[get_qstash_client] = _get_qstash_client_override
    app.dependency_overrides[get_qstash_consumer] = _get_qstash_consumer_override
    app.dependency_overrides[get_gemini_client] = _get_gemini_client_override
    app.dependency_overrides[get_browser_use_client] = _get_browser_use_client_override

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
