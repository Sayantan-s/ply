import re
import uuid

from app.core.logging.logger import get_logger
from app.modules.jdmatch.constants import (
    DROPBOX_PATTERN,
    GDRIVE_PATTERN,
)

logger = get_logger("jdmatch.utils.init_file_identity")


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
