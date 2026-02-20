from pydantic import BaseModel

from app.api.v1.dto import UIDtoModel


class ParseResumeJDInformation(UIDtoModel):
    jd_match_id: str


class AgentResponseJDVerification(BaseModel):
    is_jd: bool
    reason: str


class AgentResponseCandidateScore(BaseModel):
    score: int
    matching_skills: list[str]
    missing_skills: list[str]
    explanation: str
