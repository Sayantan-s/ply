import asyncio
import os
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import UploadFile, HTTPException
import re

# mock modules that might require environment or DB
with patch.dict(os.environ, {"API_URL": "http://localhost:8000"}):
    from app.modules.jdmatch.service import jd_match

async def test_file_upload():
    print("Testing File Upload...")
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_resume.pdf"
    mock_file.read = AsyncMock(return_value=b"fake pdf content")
    
    # Mock parse_resume to avoid writing to disk or needing repo logic dependencies
    with patch("app.modules.jdmatch.service.parse_resume") as mock_parse:
        mock_parse.return_value = {"status": "parsed"}
        
        result = await jd_match(file=mock_file)
        
        assert result == {"status": "parsed"}
        mock_file.read.assert_called_once()
        mock_parse.assert_called_once()
        # access arguments of call
        args, _ = mock_parse.call_args
        assert args[0] == b"fake pdf content" # file_content
        assert args[1] == "test_resume.pdf" # filename
        print("PASS: File Upload")

async def test_url_download():
    print("\nTesting URL Download...")
    url = "https://example.com/resume.pdf"
    
    with patch("app.modules.jdmatch.service.parse_resume") as mock_parse:
        mock_parse.return_value = {"status": "parsed_from_url"}
        
        # Mock httpx
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            
            mock_response = MagicMock()
            mock_response.content = b"downloaded content"
            mock_response.headers = {
                "content-disposition": 'attachment; filename="downloaded.pdf"',
                "content-type": "application/pdf"
            }
            mock_client.get.return_value = mock_response
            
            result = await jd_match(resume_url=url)
            
            assert result == {"status": "parsed_from_url"}
            mock_client.get.assert_called_once()
            # check parse args
            args, _ = mock_parse.call_args
            assert args[0] == b"downloaded content"
            assert args[1] == "downloaded.pdf"
            print("PASS: URL Download")

async def test_invalid_content_type():
    print("\nTesting Invalid Content Type...")
    url = "https://example.com/page.html"
    
    with patch("app.modules.jdmatch.service.parse_resume") as mock_parse:
        # Mock httpx
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            
            mock_response = MagicMock()
            mock_response.content = b"<html></html>"
            mock_response.headers = {
                "content-type": "text/html"
            }
            mock_client.get.return_value = mock_response
            
            try:
                await jd_match(resume_url=url)
                print("FAIL: Should have raised HTTPException for non-pdf")
            except HTTPException as e:
                # The detail might be wrapped or changed, checking string presence
                if "URL did not return a PDF file" in str(e.detail):
                    print("PASS: Correctly rejected non-PDF Content-Type")
                else:
                    print(f"FAIL: Raised wrong exception: {e.detail}")
            except Exception as e:
                print(f"FAIL: Raised wrong exception type: {type(e)} {e}")


async def test_gdrive_transform():
    print("\nTesting GDrive URL Transform...")
    url = "https://drive.google.com/file/d/123456789/view?usp=sharing"
    
    with patch("app.modules.jdmatch.service.parse_resume") as mock_parse:
        mock_parse.return_value = {}
        
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            
            mock_response = MagicMock()
            mock_response.content = b"content"
            mock_response.headers = {"content-type": "application/pdf"}
            mock_client.get.return_value = mock_response
            
            await jd_match(resume_url=url)
            
            # Check if URL was transformed
            call_args = mock_client.get.call_args
            called_url = call_args[0][0]
            expected_url = "https://drive.google.com/uc?export=download&id=123456789"
            
            if called_url == expected_url:
                print(f"PASS: GDrive URL Transformed correctly to {called_url}")
            else:
                print(f"FAIL: GDrive URL was {called_url}, expected {expected_url}")

async def main():
    await test_file_upload()
    await test_url_download()
    await test_invalid_content_type()
    await test_gdrive_transform()

if __name__ == "__main__":
    asyncio.run(main())
