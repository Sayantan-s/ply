from fastapi import APIRouter, UploadFile
from app.modules.jdmatch.service import jd_match
from typing import Annotated, Optional

router = APIRouter()

@router.post("")
async def jdmatch(file: UploadFile):
   return await jd_match(file)