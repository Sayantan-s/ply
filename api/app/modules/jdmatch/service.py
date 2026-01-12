from uuid import uuid4
from app.core.config import settings
from typing import Optional, Annotated
from fastapi import File
from app.modules.jdmatch.repo import parse_resume

def jd_match(file: Optional[Annotated[bytes, File()]] = None):
      file_id = uuid4().hex
      target_url = f"{settings.API_URL}/jdmatch/consumer"

      resume_info = parse_resume(file, file_id)

      return resume_info


def consumer():
      print('Consuming....')