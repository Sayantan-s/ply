from uuid import uuid4
from app.core.config import settings
from typing import Optional, Annotated
from fastapi import UploadFile, Depends
from app.modules.jdmatch.repo import save_file, init_file
from app.integrations.upstash.qstash import get_qstash_client
from qstash.client import QStash
from app.core.logging.logger import get_logger
from app.modules.jdmatch.schemas import ParseResumeJDInformation

qstash_dependency = Annotated[QStash, Depends(get_qstash_client)]
logger = get_logger("jdmatch.service")


async def jd_match(file: Optional[UploadFile] = None, resume_url: Optional[str] = None, qstash = qstash_dependency):
      logger.info("starting jd_match()")
      file_content, filename, file_id = await init_file(file, resume_url)
      
      if not file_id:
            file_id = str(uuid4())

      resume_info = save_file(file_content, filename, file_id)

      target_url = f"{settings.API_URL}/jdmatch/consumer"

      qstash.message.publish_json(
            url=target_url,
            body=resume_info.model_dump(),
      )

      logger.info("ending jd_match()")
      return file_id


async def jd_match_consumer(payload: ParseResumeJDInformation):
      logger.info("starting jd_match_consumer()")
      logger.info(f'Consuming.... {payload}')
      logger.info("ending jd_match_consumer()")