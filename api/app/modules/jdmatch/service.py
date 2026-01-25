from uuid import uuid4
from app.core.config import settings
from typing import Optional, Annotated
from fastapi import UploadFile, Depends
from app.modules.jdmatch.repo import save_file, init_file
from app.integrations.upstash.qstash import get_qstash_client
from qstash.client import QStash


qstash_dependency = Annotated[QStash, Depends(get_qstash_client)]

async def jd_match(file: Optional[UploadFile] = None, resume_url: Optional[str] = None, qstash = qstash_dependency):
      file_content, filename, file_id = await init_file(file, resume_url)
      
      if not file_id:
            file_id = str(uuid4())

      resume_info = save_file(file_content, filename, file_id)

      target_url = f"{settings.API_URL}/jdmatch/consumer"

      qstash.message.publish_json(
            url=target_url,
            body=resume_info.model_dump(),
      )

      return file_id


def consumer():
      print('Consuming....')