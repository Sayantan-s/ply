from fastapi import APIRouter, UploadFile, Form, Depends, Request
from app.modules.jdmatch.service import jd_match
from typing import Annotated, Optional
from app.integrations.upstash.qstash import get_qstash_client, get_qstash_consumer
from app.modules.jdmatch.schemas import ParseResumeJDInformation
from qstash.client import QStash
from qstash.receiver import Receiver

router = APIRouter()

@router.post("")
async def jdmatch(
   file: Optional[UploadFile] = None,
   resume_url: Optional[str] = Form(None),
   qstash: QStash = Depends(get_qstash_client)
):
   return await jd_match(file, resume_url, qstash)

@router.post("/consumer")
async def jdmatch_consumer(req: Request, receiver: Receiver = Depends(get_qstash_consumer)):
   _body = await req.body()
   signature, req_body = req.headers["Upstash-Signature"], _body.decode()
   receiver.verify(
      body=req_body,
      signature=signature
   )
   payload = ParseResumeJDInformation.model_validate_json(req_body)
   return {"status": "received", "payload": payload}