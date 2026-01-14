import os
from typing import Annotated, Optional
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.core.logging.logger import get_logger

logger = get_logger("jdmatch.repo")

def parse_resume(
    file_content: bytes,
    filename: str,
    file_id: str
):
    logger.info(f"starting parse_resume()")
    
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
        
    logger.info(f"fetched setItemRaw() > {file_name}")

    logger.info("ending parse_resume()")

    return ParseResumeJDInformation(
      candidate_resume_path=candidate_resume_path,
      file_name=file_name
    )