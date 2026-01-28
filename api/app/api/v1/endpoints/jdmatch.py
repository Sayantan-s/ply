from fastapi import APIRouter, UploadFile, Form, Depends, Request
from app.modules.jdmatch.service import jd_match, jd_match_consumer
from typing import Optional
from app.core.logging.logger import get_logger
from app.integrations.upstash.qstash import get_qstash_client, get_qstash_consumer
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from qstash.client import QStash
from qstash.receiver import Receiver

router = APIRouter()

logger = get_logger("jdmatch.api")

@router.post("")
async def jdmatch(
   file: Optional[UploadFile] = None,
   resume_url: Optional[str] = Form(None),
   qstash: QStash = Depends(get_qstash_client)
):
   logger.info("starting jdmatch()")
   response = await jd_match(file, resume_url, qstash)
   logger.info("ending jdmatch()")
   return response

@router.post("/consumer")
async def jdmatch_consumer(req: Request, receiver: Receiver = Depends(get_qstash_consumer)):
   logger.info("starting jdmatch_consumer()")
   _body = await req.body()
   signature, req_body = req.headers["Upstash-Signature"], _body.decode()
   receiver.verify(
      body=req_body,
      signature=signature
   )
   payload = ParseResumeJDInformation.model_validate_json(req_body)
   await jd_match_consumer(payload)
   logger.info("ending jdmatch_consumer()")
   return {"status": "received", "payload": payload}