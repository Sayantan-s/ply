from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class JDMatchDtl(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_id: str = Field(index=True)
    jd: str
    score: int
    missing_skills: list[str] = Field(sa_column=Column(JSON))
    matching_skills: list[str] = Field(sa_column=Column(JSON))
    explanation: str
    file_name: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
