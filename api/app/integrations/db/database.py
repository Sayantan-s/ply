import os
from collections.abc import Generator
from functools import lru_cache

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.core.logging.logger import get_logger

load_dotenv()

db_url = os.getenv("DB_URI")

engine = create_engine(db_url)

logger = get_logger("db.database")


@lru_cache(maxsize=1)
def connect_to_postgres() -> None:
    logger.info("Starting database initialization...")
    SQLModel.metadata.create_all(engine)
    logger.success("Database initialization completed")


@lru_cache(maxsize=1)
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
