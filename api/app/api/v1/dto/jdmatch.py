import uuid
from enum import Enum
from typing import Annotated, Literal

from pydantic import Field

from app.api.v1.dto import UIDtoModel
from app.modules.jdmatch.constants import JdMatchStatus

# --- SSE Event Types ---


class SSEEventType(str, Enum):
    ANALYSIS_START = "analysis_start"
    STATUS_UPDATE = "status_update"
    CONTENT_BLOCK_START = "content_block_start"
    CONTENT_BLOCK_DELTA = "content_block_delta"
    CONTENT_BLOCK_STOP = "content_block_stop"
    ANALYSIS_DELTA = "analysis_delta"
    ANALYSIS_STOP = "analysis_stop"
    ERROR = "error"


class ContentBlockType(str, Enum):
    RESULT = "result"
    EXPLANATION = "explanation"


class StopReason(str, Enum):
    COMPLETE = "complete"
    ERROR = "error"


# --- Content Block Markers ---


class ResultContentBlock(UIDtoModel):
    type: Literal[ContentBlockType.RESULT] = ContentBlockType.RESULT


class ExplanationContentBlock(UIDtoModel):
    type: Literal[ContentBlockType.EXPLANATION] = ContentBlockType.EXPLANATION


ContentBlock = Annotated[
    ResultContentBlock | ExplanationContentBlock,
    Field(discriminator="type"),
]


# --- Delta Types ---


class ResultDelta(UIDtoModel):
    type: Literal["result_delta"] = "result_delta"
    score: int
    matching_skills: list[str]
    missing_skills: list[str]


class TextDelta(UIDtoModel):
    type: Literal["text_delta"] = "text_delta"
    text: str


Delta = Annotated[
    ResultDelta | TextDelta,
    Field(discriminator="type"),
]


# --- SSE Event Models ---


class AnalysisStartEvent(UIDtoModel):
    type: Literal[SSEEventType.ANALYSIS_START] = SSEEventType.ANALYSIS_START
    analysis_id: str


class StatusUpdateEvent(UIDtoModel):
    type: Literal[SSEEventType.STATUS_UPDATE] = SSEEventType.STATUS_UPDATE
    status: JdMatchStatus


class ContentBlockStartEvent(UIDtoModel):
    type: Literal[SSEEventType.CONTENT_BLOCK_START] = SSEEventType.CONTENT_BLOCK_START
    index: int
    content_block: ContentBlock


class ContentBlockDeltaEvent(UIDtoModel):
    type: Literal[SSEEventType.CONTENT_BLOCK_DELTA] = SSEEventType.CONTENT_BLOCK_DELTA
    index: int
    delta: Delta


class ContentBlockStopEvent(UIDtoModel):
    type: Literal[SSEEventType.CONTENT_BLOCK_STOP] = SSEEventType.CONTENT_BLOCK_STOP
    index: int


class AnalysisDeltaEvent(UIDtoModel):
    type: Literal[SSEEventType.ANALYSIS_DELTA] = SSEEventType.ANALYSIS_DELTA
    stop_reason: StopReason


class AnalysisStopEvent(UIDtoModel):
    type: Literal[SSEEventType.ANALYSIS_STOP] = SSEEventType.ANALYSIS_STOP


class ErrorEvent(UIDtoModel):
    type: Literal[SSEEventType.ERROR] = SSEEventType.ERROR
    message: str


SSEEvent = (
    AnalysisStartEvent
    | StatusUpdateEvent
    | ContentBlockStartEvent
    | ContentBlockDeltaEvent
    | ContentBlockStopEvent
    | AnalysisDeltaEvent
    | AnalysisStopEvent
    | ErrorEvent
)


# --- Non-streaming Response Models (unchanged) ---


class ResumeUploadResponse(UIDtoModel):
    file_id: str
    jd_match_id: uuid.UUID


class JdResponse(UIDtoModel):
    jd_info: str
    is_link: bool


class JdMatchStatusResponse(UIDtoModel):
    status: JdMatchStatus


class JdMatchAnalysisResponse(UIDtoModel):
    jd_match_id: uuid.UUID
    status: str
    score: int | None = None
    matching_skills: list[str] | None = None
    missing_skills: list[str] | None = None
    explanation: str | None = None
