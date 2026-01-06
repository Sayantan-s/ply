from uuid import uuid4
from app.core.config import settings
from typing import Annotated, Optional
from fastapi import File

def jd_match(file: Optional[Annotated[bytes, File()]] = None):
      file_id = uuid4().hex
      target_url = f"{settings.API_URL}/jdmatch/consumer"

      return {"file_size": len(file) if file else 'No file uploaded'}


def consumer():
      print('Consuming....')