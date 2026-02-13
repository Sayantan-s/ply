import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.core.logging.logger import get_logger

load_dotenv()

db_url = os.getenv("DB_URI")

engine = create_engine(db_url)

logger = get_logger("db.database")


def init_db() -> None:
    logger.info("Starting database initialization...")
    SQLModel.metadata.create_all(engine)
    logger.success("Database initialization completed")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
