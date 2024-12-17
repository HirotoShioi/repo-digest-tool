from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

# Global engine variable to be used across the application
engine: Optional[Engine] = None


def init_db(database_url: str = "sqlite:///repo_tool.db") -> None:
    """Initialize the database engine"""
    global engine
    if engine is None:
        engine = create_engine(database_url)
        SQLModel.metadata.create_all(engine)


def get_engine() -> Engine:
    """Get the database engine"""
    if engine is None:
        raise RuntimeError("Database engine not initialized")
    return engine


def get_session() -> Generator[Session, None, None]:
    """Get a database session"""
    if engine is None:
        raise RuntimeError("Database engine not initialized")
    with Session(engine) as session:
        yield session


def dispose_db() -> None:
    """Dispose the database engine"""
    global engine
    if engine:
        engine.dispose()
        engine = None
