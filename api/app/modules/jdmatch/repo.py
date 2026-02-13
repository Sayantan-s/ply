from typing import Any

from sqlmodel import Session

from app.integrations.db.models import JDMatchDtl


async def save_jd_match_info(
    _db_session: Session,
    jd: str,
    file_id: str,
    file_name: str,
    score_data: dict[str, Any],
) -> None:
    jd_match_dtl = JDMatchDtl(
        file_id=file_id,
        jd=jd,
        file_name=file_name,
        score=score_data["score"],
        matching_skills=score_data["matching_skills"],
        missing_skills=score_data["missing_skills"],
        explanation=score_data["explanation"],
    )
    _db_session.add(jd_match_dtl)
    _db_session.commit()
    _db_session.refresh(jd_match_dtl)
