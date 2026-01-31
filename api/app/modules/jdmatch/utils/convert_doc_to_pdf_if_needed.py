import os
import tempfile

from fastapi import HTTPException

from app.core.logging.logger import get_logger
from app.modules.jdmatch.utils.doc_to_pdf import doc_to_pdf

logger = get_logger("jdmatch.utils.convert_doc_to_pdf_if_needed")


async def convert_doc_to_pdf_if_needed(
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
        logger.error(f"Conversion failed: {e!s}")
        raise HTTPException(
            status_code=500, detail=f"Failed to convert document to PDF: {e!s}"
        )
