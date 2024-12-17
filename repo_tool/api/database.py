from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

# Global engine variable to be used across the application
engine = create_engine("sqlite:///repo_tool.db")


def init_db() -> None:
    """Initialize the database engine"""
    SQLModel.metadata.create_all(engine)


def get_engine() -> Engine:
    """Get the database engine"""
    return engine


def get_session() -> Generator[Session, None, None]:
    """Get a database session"""
    with Session(engine) as session:
        yield session


def dispose_db() -> None:
    """Dispose the database engine"""
    engine.dispose()
