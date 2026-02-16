from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_upload_resume_file(client):
    with patch(
        "app.api.v1.endpoints.jdmatch.upload_resume", new_callable=AsyncMock
    ) as mock_upload:
        mock_upload.return_value = {
            "file_id": "test_id",
            "signed_url": "http://test.com",
        }

        files = {"resume_file": ("resume.pdf", b"content", "application/pdf")}
        response = await client.post("/api/v1/jdmatch/resume/upload", files=files)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "file_id": "test_id",
            "signed_url": "http://test.com",
        }
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_upload_resume_url(client):
    with patch(
        "app.api.v1.endpoints.jdmatch.upload_resume", new_callable=AsyncMock
    ) as mock_upload:
        mock_upload.return_value = {
            "file_id": "test_id",
            "signed_url": "http://test.com",
        }

        data = {"resume_url": "http://resume.com/file.pdf"}
        response = await client.post("/api/v1/jdmatch/resume/upload", data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "file_id": "test_id",
            "signed_url": "http://test.com",
        }
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_add_jd(client):
    with patch(
        "app.api.v1.endpoints.jdmatch.process_jd", new_callable=AsyncMock
    ) as mock_process:
        mock_process.return_value = {"jd_info": "Software Engineer", "is_link": False}

        data = {"jd_info": "Software Engineer"}
        response = await client.patch("/api/v1/jdmatch/test_file_id/jd/add", data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"jd_info": "Software Engineer", "is_link": False}
        mock_process.assert_called_once()


@pytest.mark.asyncio
async def test_jd_match_init(client):
    with patch(
        "app.api.v1.endpoints.jdmatch.jd_match_init", new_callable=AsyncMock
    ) as mock_init:
        mock_init.return_value = {"file_id": "test_file_id"}

        response = await client.post("/api/v1/jdmatch/test_file_id/init")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == {"file_id": "test_file_id"}
        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_jd_match_consumer(client, mock_receiver):
    with patch(
        "app.api.v1.endpoints.jdmatch.jd_match_analyze", new_callable=AsyncMock
    ) as mock_analyze:
        mock_receiver.verify.return_value = None

        payload = {
            "file_id": "test_file_id",
            "jd_info": "Software Engineer",
            "is_link": False,
        }

        headers = {"Upstash-Signature": "test_sig"}
        response = await client.post(
            "/api/v1/jdmatch/consumer", json=payload, headers=headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "received"
        mock_analyze.assert_called_once()
