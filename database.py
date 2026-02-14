from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator


SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:lanadelrey@localhost:5432/passkeeper'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, echo=True, pool_size=5, max_overflow=10)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()