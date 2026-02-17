from typing import Generic, Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

# Define a Type Variable for our Data payload
T = TypeVar("T")


class UIDtoModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ResponseEnvelope(UIDtoModel, Generic[T]):
    success: bool
    data: T | None = None
    error: list[str] | None = None
    request_id: str = Field(default_factory=lambda: uuid4().hex)

    @classmethod
    def ok(cls, data: T):
        return cls(success=True, data=data, error=None)
