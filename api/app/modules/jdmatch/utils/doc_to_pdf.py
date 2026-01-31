import os

import httpx

from app.core.config import settings
from app.core.logging.logger import get_logger

logger = get_logger("jdmatch.utils.doc_to_pdf")


async def doc_to_pdf(file_path: str) -> bytes:
    """
    Convert .doc, .docx to pdf
    """
    url = f"{settings.DOC_TO_PDF_API_URL}/forms/libreoffice/convert"

    async with httpx.AsyncClient() as client:
        try:
            with open(file_path, "rb") as f:
                files = {"files": (os.path.basename(file_path), f)}
                logger.info(f"Converting {file_path} to PDF via {url}")
                response = await client.post(url, files=files)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"Failed to convert doc to pdf: {e!s}")
            raise e
