from fastapi import APIRouter, UploadFile, Form, Depends, Request
from app.modules.jdmatch.service import jd_match
from typing import Annotated, Optional
from app.integrations.upstash.qstash import get_qstash_client
from qstash.client import QStash

router = APIRouter()

@router.post("")
async def jdmatch(
   file: Optional[UploadFile] = None,
   resume_url: Optional[str] = Form(None),
   qstash: QStash = Depends(get_qstash_client)
):
   return await jd_match(file, resume_url, qstash)

@router.post("/consumer")
async def jdmatch_consumer(request: Request):
    body = await request.body()
    print(f"Received payload: {body.decode()}")
    return {"status": "received"}