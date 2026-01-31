import re
from urllib.parse import unquote, urlparse

import httpx

from app.core.logging.logger import get_logger
from app.modules.jdmatch.constants import DEFAULT_FILENAME

logger = get_logger("jdmatch.utils.extract_filename_from_response")


def extract_filename_from_response(response: httpx.Response, original_url: str) -> str:
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
