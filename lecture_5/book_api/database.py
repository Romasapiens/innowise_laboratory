from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# SQLite database file
SQLALCHEMY_DATABASE_URL: str = "sqlite:///./books.db"

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Session factory
SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Ensures:
        Session is properly closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()