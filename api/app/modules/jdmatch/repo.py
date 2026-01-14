import os
from typing import Annotated, Optional
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from app.core.logging.logger import get_logger
import httpx
import re
from fastapi import HTTPException

logger = get_logger("jdmatch.repo")

def save_file(
    file_content: bytes,
    filename: str,
    file_id: str
) -> ParseResumeJDInformation:
    logger.info(f"starting save_file()")
    
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
      file_name=file_name
    )

async def init_file(file, resume_url):
    logger.info(f"starting init_file() > file={file.filename if file else 'None'}, resume_url={resume_url}")
    if not file and not resume_url:
          logger.error("No file or resume_url provided")
          raise HTTPException(status_code=400, detail="Either file or resume_url must be provided")
    
    file_content = None
    filename = "downloaded_resume.pdf" # Default fallback
    
    if file:
          logger.info(f"Processing uploaded file: {file.filename}")
          file_content = await file.read()
          filename = file.filename
    elif resume_url:
          logger.info(f"Processing resume_url: {resume_url}")
          # Handle URL transformations for direct download
          download_url = resume_url
    
          # Dropbox
          if "dropbox.com" in download_url:
                logger.debug("Detected Dropbox URL, modifying for direct download")
                download_url = download_url.replace("?dl=0", "?dl=1")
    
          # Google Drive
          # Convert https://drive.google.com/file/d/ID/view... to https://drive.google.com/uc?export=download&id=ID
          gdrive_pattern = r"drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)"
          match = re.search(gdrive_pattern, download_url)
          if match:
                file_id = match.group(1)
                logger.debug(f"Detected Google Drive URL, extracted file_id: {file_id}")
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
          async with httpx.AsyncClient() as client:
                try:
                      logger.info(f"Downloading from URL: {download_url}")
                      response = await client.get(download_url, follow_redirects=True)
                      response.raise_for_status()
    
                      # Validate Content-Type
                      content_type = response.headers.get("content-type", "")
                      logger.debug(f"Download Content-Type: {content_type}")
                      if "application/pdf" not in content_type and "application/octet-stream" not in content_type:
                            logger.error(f"Invalid Content-Type: {content_type}")
                            # Only loose check for octet-stream as some servers might misconfigure
                            raise HTTPException(status_code=400, detail="URL did not return a PDF file")
    
                      file_content = response.content
    
                      # Try to get filename from Content-Disposition
                      content_disposition = response.headers.get("content-disposition")
                      if content_disposition:
                            fname_match = re.search(r'filename="?([^"]+)"?', content_disposition)
                            if fname_match:
                                  filename = fname_match.group(1)
    
                      # Fallback if filename is still default and we have a path in url
                      if filename == "downloaded_resume.pdf" and response.url.path:
                            path_filename = response.url.path.split("/")[-1]
                            if path_filename and path_filename.lower().endswith(".pdf"):
                                  filename = path_filename
    
                except HTTPException as he:
                      raise he
                except Exception as e:
                      logger.error(f"Download failed: {str(e)}")
                      raise HTTPException(status_code=400, detail=f"Failed to download resume from URL: {str(e)}")
    return file_content, filename, file_id