import httpx
from fastapi import HTTPException

from app.core.logging.logger import get_logger
from app.modules.jdmatch.utils.extract_filename_from_response import (
    extract_filename_from_response,
)
from app.modules.jdmatch.utils.transform_download_url import (
    transform_download_url,
)

logger = get_logger("jdmatch.utils.download_resume")


async def download_resume(resume_url: str) -> tuple[bytes, str, str | None]:
    """Download resume from URL and determine filename/file_id."""
    download_url, file_id = transform_download_url(resume_url)

    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Downloading from URL: {download_url}")
            response = await client.get(download_url, follow_redirects=True)
            response.raise_for_status()

            # Validate Content-Type
            content_type = response.headers.get("content-type", "")
            logger.debug(f"Download Content-Type: {content_type}")
            supported_types = [
                "application/pdf",
                "application/octet-stream",
                "officedocument",
                "msword",
            ]
            if not any(t in content_type for t in supported_types):
                logger.error(f"Invalid Content-Type: {content_type}")
                raise HTTPException(
                    status_code=400,
                    detail="URL did not return a supported file (PDF, DOC, DOCX)",
                )

            file_content = response.content
            filename = extract_filename_from_response(response, download_url)
            return file_content, filename, file_id

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Download failed: {e!s}")
            raise HTTPException(
                status_code=400, detail=f"Failed to download resume from URL: {e!s}"
            )
