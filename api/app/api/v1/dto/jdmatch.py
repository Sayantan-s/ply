from pydantic import BaseModel


class JdMatchResponse(BaseModel):
    file_id: str


class ResumeUploadResponse(BaseModel):
    file_id: str
    signed_url: str


class JdResponse(BaseModel):
    jd_info: str
    is_link: bool
