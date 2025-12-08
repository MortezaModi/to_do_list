from typing import Generator
from app.db.session import get_db_context
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    """Dependency for getting a DB session."""
    try:
        with get_db_context() as db:
            yield db
    except Exception as e:
        # Note: Exception handling for database failures should be robust
        # This will be caught by FastAPI's global exception handler
        raise e
