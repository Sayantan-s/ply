import uuid
from enum import Enum
from typing import Literal

from pydantic import Field

from app.api.v1.dto import UIDtoModel
from app.modules.jdmatch.constants import JdMatchStatus


class StreamType(str, Enum):
    STATUS = "status"
    ANALYSIS = "analysis"
    RESULT = "result"
    EXPLANATION = "explanation"


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


class ResultStreamResponse(UIDtoModel):
    type: Literal[StreamType.RESULT] = StreamType.RESULT
    score: int
    matching_skills: list[str]
    missing_skills: list[str]


class ExplanationStreamResponse(UIDtoModel):
    type: Literal[StreamType.EXPLANATION] = StreamType.EXPLANATION
    chunk: str


class JdMatchStreamResponse(UIDtoModel):
    payload: (
        StatusStreamResponse
        | AnalysisStreamResponse
        | ResultStreamResponse
        | ExplanationStreamResponse
    ) = Field(..., discriminator="type")


class JdMatchAnalysisResponse(UIDtoModel):
    jd_match_id: uuid.UUID
    status: str
    score: int | None = None
    matching_skills: list[str] | None = None
    missing_skills: list[str] | None = None
    explanation: str | None = None
