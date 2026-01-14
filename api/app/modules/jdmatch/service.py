from uuid import uuid4
from app.core.config import settings
from typing import Optional, Annotated
from fastapi import UploadFile, HTTPException
import httpx
import re
from app.modules.jdmatch.repo import parse_resume

async def jls_extract_def(file, resume_url):
    if not file and not resume_url:
          raise HTTPException(status_code=400, detail="Either file or resume_url must be provided")
    
    file_content = None
    filename = "downloaded_resume.pdf" # Default fallback
    
    if file:
          file_content = await file.read()
          filename = file.filename
    elif resume_url:
          # Handle URL transformations for direct download
          download_url = resume_url
    
          # Dropbox
          if "dropbox.com" in download_url:
                download_url = download_url.replace("?dl=0", "?dl=1")
    
          # Google Drive
          # Convert https://drive.google.com/file/d/ID/view... to https://drive.google.com/uc?export=download&id=ID
          gdrive_pattern = r"drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)"
          match = re.search(gdrive_pattern, download_url)
          if match:
                file_id = match.group(1)
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
          async with httpx.AsyncClient() as client:
                try:
                      response = await client.get(download_url, follow_redirects=True)
                      response.raise_for_status()
    
                      # Validate Content-Type
                      content_type = response.headers.get("content-type", "")
                      if "application/pdf" not in content_type and "application/octet-stream" not in content_type:
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
                      raise HTTPException(status_code=400, detail=f"Failed to download resume from URL: {str(e)}")
    return file_content, filename, file_id


async def jd_match(file: Optional[UploadFile] = None, resume_url: Optional[str] = None):
      file_content, filename, file_id = await jls_extract_def(file, resume_url)

      target_url = f"{settings.API_URL}/jdmatch/consumer"

      resume_info = parse_resume(file_content, filename, file_id)

      return resume_info


def consumer():
      print('Consuming....')