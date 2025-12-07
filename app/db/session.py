import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager #added half way
from app.utils.config import Config # added at the very end

load_dotenv() # finds .env

DATABASE_URL = os.getenv("DATABASE_URL") # retrieve connection

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

"""
engine = create_engine(
    DATABASE_URL,
    echo=False, # True= see SQL logs
    pool_pre_ping=True # tests connection before using it
)
"""

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    pass