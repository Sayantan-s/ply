from pydantic import BaseModel


class JdMatchResponse(BaseModel):
    file_id: str
