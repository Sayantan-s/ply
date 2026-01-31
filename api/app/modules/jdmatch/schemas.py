from pydantic import BaseModel


class ParseResumeJDInformation(BaseModel):
    candidate_resume_path: str
    file_name: str
    jd_info: str


class AgentResponseJDVerification(BaseModel):
    is_jd: bool
    reason: str


class AgentResponseCandidateScore(BaseModel):
    score: int
    matching_skills: list[str]
    missing_skills: list[str]
    explanation: str
