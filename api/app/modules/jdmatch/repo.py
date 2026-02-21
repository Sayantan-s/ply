from datetime import datetime
from typing import Any

from sqlmodel import Session, select

from app.integrations.db.models import JDMatchDtl
from app.modules.jdmatch.constants import JdMatchStatus


async def create_jd_match_record(
    _db_session: Session,
    file_id: str,
    file_name: str,
    resume_url: str,
    jd_info: str | None = None,
) -> JDMatchDtl:
    jd_match_dtl = JDMatchDtl(
        file_id=file_id,
        file_name=file_name,
        resume_url=resume_url,
        jd=jd_info,
    )
    _db_session.add(jd_match_dtl)
    _db_session.commit()
    _db_session.refresh(jd_match_dtl)
    return jd_match_dtl


async def update_jd_info(
    _db_session: Session,
    jd_match_id: str,
    jd_info: str,
) -> JDMatchDtl | None:
    statement = select(JDMatchDtl).where(JDMatchDtl.id == jd_match_id)
    results = _db_session.exec(statement)
    jd_match_dtl = results.first()
    if jd_match_dtl:
        jd_match_dtl.jd = jd_info
        jd_match_dtl.updated_at = datetime.now()
        _db_session.add(jd_match_dtl)
        _db_session.commit()
        _db_session.refresh(jd_match_dtl)
    return jd_match_dtl


async def update_jd_match_status(
    _db_session: Session,
    jd_match_id: str,
    status: str,
) -> JDMatchDtl | None:
    statement = select(JDMatchDtl).where(JDMatchDtl.id == jd_match_id)
    results = _db_session.exec(statement)
    jd_match_dtl = results.first()
    if jd_match_dtl:
        jd_match_dtl.status = status
        jd_match_dtl.updated_at = datetime.now()
        _db_session.add(jd_match_dtl)
        _db_session.commit()
        _db_session.refresh(jd_match_dtl)
    return jd_match_dtl


async def get_jd_match_by_file_id(
    _db_session: Session,
    file_id: str,
) -> JDMatchDtl | None:
    statement = select(JDMatchDtl).where(JDMatchDtl.file_id == file_id)
    results = _db_session.exec(statement)
    return results.first()


async def get_jd_match_by_jd_match_id(
    _db_session: Session,
    jd_match_id: str,
) -> JDMatchDtl | None:
    statement = select(JDMatchDtl).where(JDMatchDtl.id == jd_match_id)
    results = _db_session.exec(statement)
    return results.first()


async def save_jd_match_info(
    _db_session: Session,
    jd_match_id: str,
    jd: str,
    score_data: dict[str, Any],
) -> None:
    statement = select(JDMatchDtl).where(JDMatchDtl.id == jd_match_id)
    results = _db_session.exec(statement)
    jd_match_dtl = results.first()

    if not jd_match_dtl:
        raise ValueError(f"No record found for jd_match_id: {jd_match_id}")

    jd_match_dtl.jd = jd
    jd_match_dtl.score = score_data["score"]
    jd_match_dtl.matching_skills = score_data["matching_skills"]
    jd_match_dtl.missing_skills = score_data["missing_skills"]
    jd_match_dtl.explanation = score_data["explanation"]
    jd_match_dtl.status = JdMatchStatus.MATCHED.value
    jd_match_dtl.updated_at = datetime.now()

    _db_session.add(jd_match_dtl)
    _db_session.commit()
    _db_session.refresh(jd_match_dtl)
