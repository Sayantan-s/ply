import uuid
from typing import Literal, Union

from pydantic import BaseModel, Field

from app.api.v1.dto import UIDtoModel
from app.modules.jdmatch.constants import JdMatchStatus


class ResumeUploadResponse(UIDtoModel):
    file_id: str
    jd_match_id: uuid.UUID


class JdResponse(UIDtoModel):
    jd_info: str
    is_link: bool


class JdMatchStatusResponse(UIDtoModel):
    status: JdMatchStatus


class StatusStreamResponse(BaseModel):
    type: Literal["status"] = "status"
    status: JdMatchStatus


class AnalysisStreamResponse(BaseModel):
    type: Literal["analysis"] = "analysis"
    chunk: str


class JdMatchStreamResponse(BaseModel):
    payload: Union[StatusStreamResponse, AnalysisStreamResponse] = Field(..., discriminator="type")
