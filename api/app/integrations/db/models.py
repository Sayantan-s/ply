import uuid
from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.modules.jdmatch.constants import JdMatchStatus


class JDMatchDtl(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    file_id: str = Field(index=True, unique=True)
    jd: str | None = None
    status: str = Field(default=JdMatchStatus.QUEUED.value)
    score: int | None = None
    missing_skills: list[str] | None = Field(default=None, sa_column=Column(JSON))
    matching_skills: list[str] | None = Field(default=None, sa_column=Column(JSON))
    explanation: str | None = None
    file_name: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    resume_url: str | None = None
