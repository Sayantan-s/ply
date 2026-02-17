import uuid

from pydantic import BaseModel, Field

from app.api.v1.dto import UIDtoModel


class JdMatchResponse(UIDtoModel):
    file_id: str


class ResumeUploadResponse(UIDtoModel):
    file_id: str
    jd_match_id: uuid.UUID


class JdResponse(UIDtoModel):
    jd_info: str
    is_link: bool


class WebhookHeaders(BaseModel):
    # Pydantic automatically handles the hyphen-to-underscore conversion
    upstash_signature: str = Field(alias="Upstash-Signature")
