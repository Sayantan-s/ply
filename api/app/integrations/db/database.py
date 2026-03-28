from collections.abc import Generator
from functools import lru_cache

from app.core.config import settings
from sqlmodel import Session, SQLModel, create_engine

from app.core.logging.logger import get_logger

engine = create_engine(settings.DB_URI)

logger = get_logger("db.database")


@lru_cache(maxsize=1)
def connect_to_postgres() -> None:
    logger.info("Starting database initialization...")
    SQLModel.metadata.create_all(engine)
    logger.success("Database initialization completed")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
