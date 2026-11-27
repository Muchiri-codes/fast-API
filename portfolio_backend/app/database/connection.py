
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL, #major
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800
)


SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
