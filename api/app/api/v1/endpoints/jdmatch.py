from fastapi import APIRouter, File
from app.modules.jdmatch.service import jd_match
from typing import Annotated, Optional

router = APIRouter()

@router.post("")
def jdmatch(file: Optional[Annotated[bytes, File()]] = None):
   return jd_match(file)