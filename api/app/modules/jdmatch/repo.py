from sqlmodel import Session

from app.integrations.db.database import engine
from app.integrations.db.models import JDMatchDtl


async def save_jd_match_info(
    jd: str, file_id: str, file_name: str, score_data: dict
) -> None:
    with Session(engine) as session:
        jd_match_dtl = JDMatchDtl(
            file_id=file_id,
            jd=jd,
            file_name=file_name,
            score=score_data["score"],
            matching_skills=score_data["matching_skills"],
            missing_skills=score_data["missing_skills"],
            explanation=score_data["explanation"],
        )
        session.add(jd_match_dtl)
        session.commit()
        session.refresh(jd_match_dtl)
