import uuid

from fastapi import HTTPException

from app.core.logging.logger import get_logger
from app.modules.jdmatch.utils.convert_doc_to_pdf_if_needed import (
    convert_doc_to_pdf_if_needed,
)
from app.modules.jdmatch.utils.download_resume import download_resume

logger = get_logger("jdmatch.utils.init_file")


async def init_file(file, resume_url, file_id: str | None = None):
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
        file_content, filename, _file_id = await download_resume(resume_url)
        # Use the provided file_id if it exists, otherwise use the one from download
        file_id = file_id or _file_id or str(uuid.uuid4())

    file_content, filename = await convert_doc_to_pdf_if_needed(file_content, filename)

    return file_content, filename, file_id
