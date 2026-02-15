from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class JDMatchDtl(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_id: str = Field(index=True, unique=True)
    jd: str | None = None
    score: int | None = None
    missing_skills: list[str] | None = Field(default=None, sa_column=Column(JSON))
    matching_skills: list[str] | None = Field(default=None, sa_column=Column(JSON))
    explanation: str | None = None
    file_name: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
