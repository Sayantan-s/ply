from fastapi import APIRouter, UploadFile, Form
from app.modules.jdmatch.service import jd_match
from typing import Annotated, Optional

router = APIRouter()

@router.post("")
async def jdmatch(
   file: Optional[UploadFile] = None,
   resume_url: Optional[str] = Form(None)
):
   return await jd_match(file, resume_url)