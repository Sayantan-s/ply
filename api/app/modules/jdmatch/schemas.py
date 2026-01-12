from pydantic import BaseModel

class ParseResumeJDInformation(BaseModel):
    candidate_resume_path: str
    file_name: str