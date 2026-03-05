import uuid
from enum import Enum
from typing import Literal

from pydantic import Field

from app.api.v1.dto import UIDtoModel
from app.modules.jdmatch.constants import JdMatchStatus


class StreamType(str, Enum):
    STATUS = "status"
    ANALYSIS = "analysis"


class ResumeUploadResponse(UIDtoModel):
    file_id: str
    jd_match_id: uuid.UUID


class JdResponse(UIDtoModel):
    jd_info: str
    is_link: bool


class JdMatchStatusResponse(UIDtoModel):
    status: JdMatchStatus


class StatusStreamResponse(UIDtoModel):
    type: Literal[StreamType.STATUS] = StreamType.STATUS
    status: JdMatchStatus


class AnalysisStreamResponse(UIDtoModel):
    type: Literal[StreamType.ANALYSIS] = StreamType.ANALYSIS
    chunk: str


class JdMatchStreamResponse(UIDtoModel):
    payload: StatusStreamResponse | AnalysisStreamResponse = Field(
        ..., discriminator="type"
    )
