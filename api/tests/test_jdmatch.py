from unittest.mock import AsyncMock, patch
import uuid
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_jd_match(client):
    with patch(
        "app.api.v1.endpoints.jdmatch.create_jd_match", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = {
            "file_id": "test_id",
            "jd_match_id": uuid.uuid4(),
        }

        files = {"resume_file": ("resume.pdf", b"content", "application/pdf")}
        data = {"jd_info": "Software Engineer"}
        response = await client.post("/api/v1/jdmatch/", files=files, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        json_data = response.json()
        assert json_data["success"] is True
        assert json_data["data"]["file_id"] == "test_id"
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_jd_match_streaming(client):
    async def mock_generator(*args, **kwargs):
        from app.api.v1.dto.jdmatch import JdMatchStreamResponse, StatusStreamResponse, AnalysisStreamResponse
        from app.modules.jdmatch.constants import JdMatchStatus
        
        yield JdMatchStreamResponse(payload=StatusStreamResponse(status=JdMatchStatus.ANALYZING))
        yield JdMatchStreamResponse(payload=AnalysisStreamResponse(chunk="test chunk"))
        yield JdMatchStreamResponse(payload=StatusStreamResponse(status=JdMatchStatus.MATCHED))

    with patch(
        "app.api.v1.endpoints.jdmatch.jd_match_analyze", side_effect=mock_generator
    ) as mock_analyze:
        jd_match_id = str(uuid.uuid4())
        response = await client.post(f"/api/v1/jdmatch/{jd_match_id}/analyze")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/x-ndjson"
        
        lines = [line for line in response.iter_lines() if line]
        assert len(lines) == 3
        mock_analyze.assert_called_once()


@pytest.mark.asyncio
async def test_get_jd_match_status(client):
    with patch(
        "app.api.v1.endpoints.jdmatch.get_jd_match_status", new_callable=AsyncMock
    ) as mock_status:
        from app.modules.jdmatch.constants import JdMatchStatus
        mock_status.return_value = {"status": JdMatchStatus.MATCHED}

        jd_match_id = str(uuid.uuid4())
        response = await client.get(f"/api/v1/jdmatch/{jd_match_id}/status")

        assert response.status_code == status.HTTP_200_OK
        json_data = response.json()
        assert json_data["success"] is True
        assert json_data["data"]["status"] == JdMatchStatus.MATCHED.value
        mock_status.assert_called_once()
