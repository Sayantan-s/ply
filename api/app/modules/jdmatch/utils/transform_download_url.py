import re

from app.core.logging.logger import get_logger
from app.modules.jdmatch.constants import (
    DROPBOX_PATTERN,
    GDRIVE_PATTERN,
)

logger = get_logger("jdmatch.utils.transform_download_url")


def transform_download_url(resume_url: str) -> tuple[str, str | None]:
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
