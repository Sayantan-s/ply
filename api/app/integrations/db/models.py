import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class JDMatchDtl(SQLModel, table=True):
    id: int | None = Field(default=uuid.uuid4(), primary_key=True)
    file_id: str = Field(index=True)
    jd: str
    score: int
    missing_skills: list[str]
    matching_skills: list[str]
    explanation: str
    file_name: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
