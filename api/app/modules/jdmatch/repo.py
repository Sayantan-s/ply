import os
import tempfile
from urllib.parse import urlparse, unquote
from typing import Optional
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.core.logging.logger import get_logger
from app.modules.jdmatch.constants import (
    GDRIVE_PATTERN,
    DROPBOX_PATTERN,
    DEFAULT_FILENAME,
)
import httpx
import re
from fastapi import HTTPException
from app.core.config import settings
import uuid


logger = get_logger("jdmatch.repo")


def save_file(
    file_content: bytes, jd_info: str, filename: str, file_id: str
) -> ParseResumeJDInformation:
    logger.info("starting save_file()")

    if not file_content:
        logger.error("No file content provided")
        raise ValueError("No file content provided")

    file_name = f"{file_id}-{filename}"

    logger.info(f"getting setItemRaw() > {file_name}")

    root_project_path = os.getcwd()
    upload_dir = os.path.join(root_project_path, "public", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    candidate_resume_path = os.path.join(upload_dir, file_name)

    with open(candidate_resume_path, "wb") as f:
        f.write(file_content)

    logger.info("ending save_file()")

    return ParseResumeJDInformation(
        candidate_resume_path=candidate_resume_path,
        file_name=file_name,
        jd_info=jd_info,
    )


def _transform_download_url(resume_url: str) -> tuple[str, Optional[str]]:
    """Handle URL transformations for direct download (Dropbox, Google Drive)."""
    download_url = resume_url
    file_id = None

    # Dropbox
    dbx_match = re.search(DROPBOX_PATTERN, download_url)
    if dbx_match:
        file_id = dbx_match.group(1)
        logger.debug(f"Detected Dropbox URL, extracted file_id: {file_id}")
        if "?dl=0" in download_url:
            download_url = download_url.replace("?dl=0", "?dl=1")
        elif "?dl=" not in download_url:
            download_url += "?dl=1"

    # Google Drive / Docs
    g_match = re.search(GDRIVE_PATTERN, download_url)
    if g_match:
        file_id = g_match.group(1)
        logger.debug(f"Detected Google Drive/Docs URL, extracted file_id: {file_id}")
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    return download_url, file_id


def _extract_filename_from_response(response: httpx.Response, original_url: str) -> str:
    """Extract filename from Content-Disposition header, response path, or original URL."""
    filename = DEFAULT_FILENAME  # Default fallback

    # Try to get filename from Content-Disposition
    content_disposition = response.headers.get("content-disposition")
    if content_disposition:
        fname_match = re.search(r'filename="?([^"]+)"?', content_disposition)
        if fname_match:
            return fname_match.group(1)

    # Fallback if we have a path in response URL
    if response.url.path:
        path_filename = unquote(response.url.path.split("/")[-1])
        if path_filename and path_filename.lower().endswith((".pdf", ".doc", ".docx")):
            return path_filename

    # Fallback if we have a path in original URL
    try:
        parsed_url = urlparse(original_url)
        path_filename = unquote(parsed_url.path.split("/")[-1])
        if path_filename and path_filename.lower().endswith((".pdf", ".doc", ".docx")):
            return path_filename
    except Exception as e:
        logger.warning(f"Failed to parse filename from download_url: {e}")

    return filename


async def _download_resume(resume_url: str) -> tuple[bytes, str, Optional[str]]:
    """Download resume from URL and determine filename/file_id."""
    download_url, file_id = _transform_download_url(resume_url)

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
            filename = _extract_filename_from_response(response, download_url)
            return file_content, filename, file_id

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Failed to download resume from URL: {str(e)}"
            )


async def _convert_doc_to_pdf_if_needed(
    file_content: bytes, filename: str
) -> tuple[bytes, str]:
    """Convert .doc, .docx to pdf if needed."""
    if not filename.lower().endswith((".doc", ".docx")):
        return file_content, filename

    logger.info(f"Converting {filename} to PDF")
    try:
        with tempfile.NamedTemporaryFile(
            suffix=os.path.splitext(filename)[1], delete=False
        ) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            pdf_content = await doc_to_pdf(tmp_path)
            new_filename = os.path.splitext(filename)[0] + ".pdf"
            return pdf_content, new_filename
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                logger.debug(f"Cleaned up temp file {tmp_path}")

    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to convert document to PDF: {str(e)}"
        )


def init_file_identity(resume_url: str):
    file_id = None
    if resume_url:
        g_match = re.search(GDRIVE_PATTERN, resume_url)
        dbx_match = re.search(DROPBOX_PATTERN, resume_url)

        if g_match:
            file_id = g_match.group(1)
            logger.debug(f"Early extracted GDrive/Docs file_id: {file_id}")
        elif dbx_match:
            file_id = dbx_match.group(1)
            logger.debug(f"Early extracted Dropbox file_id: {file_id}")

    if not file_id:
        file_id = str(uuid.uuid4())
        logger.debug(f"Generated early file_id: {file_id}")
    return file_id


async def init_file(file, resume_url, file_id: Optional[str] = None):
    logger.info(
        f"starting init_file() > file={file.filename if file else 'None'}, resume_url={resume_url}"
    )

    if not file and not resume_url:
        logger.error("No file or resume_url provided")
        raise HTTPException(
            status_code=400, detail="Either file or resume_url must be provided"
        )

    if file:
        logger.info(f"Processing uploaded file: {file.filename}")
        file_content = await file.read()
        filename = file.filename
        file_id = file_id or str(uuid.uuid4())
    else:
        logger.info(f"Processing resume_url: {resume_url}")
        file_content, filename, _file_id = await _download_resume(resume_url)
        # Use the provided file_id if it exists, otherwise use the one from download
        file_id = file_id or _file_id or str(uuid.uuid4())

    file_content, filename = await _convert_doc_to_pdf_if_needed(file_content, filename)

    return file_content, filename, file_id


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
            logger.error(f"Failed to convert doc to pdf: {str(e)}")
            raise e
