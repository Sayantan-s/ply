from pathlib import Path

from app.core.logging.logger import get_logger

logger = get_logger("jdmatch.utils.cleanup_file")


def cleanup_file(candidate_resume_path: str):
    # Cleanup: removes the file from local storage after processing
    resume_path = Path(candidate_resume_path)
    if resume_path.exists():
        resume_path.unlink()
        logger.info("Cleaned up resume file: %s", candidate_resume_path)
    return resume_path
