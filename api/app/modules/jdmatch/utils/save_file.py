import os

from app.core.logging.logger import get_logger
from app.modules.jdmatch.schemas import ParseResumeJDInformation

logger = get_logger("jdmatch.utils.save_file")


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
