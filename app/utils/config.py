import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Central configuration settings for the ToDoList application.
    """

    # --- Database Configuration ---

    # Retrieves the DB URL from environment variables, defaulting to a local SQLite file.
    # This is essential for the DB Layer and Alembic.
    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Morteza82@localhost:5432/todolist"
    )

    # --- Project Model Constraints (Used for Service Layer Validation) ---

    PROJECT_NAME_MIN_WORDS: int = 1
    PROJECT_NAME_MAX_WORDS: int = 5
    PROJECT_DESCRIPTION_MAX_WORDS: int = 20

    # --- Task Model Constraints (Used for Service Layer Validation) ---

    TASK_TITLE_MIN_WORDS: int = 1
    TASK_TITLE_MAX_WORDS: int = 10
    TASK_DESCRIPTION_MIN_WORDS: int = 1
    TASK_DESCRIPTION_MAX_WORDS: int = 30

    # --- General Utilities ---

    # This is used by the CLI to show valid choices.
    @staticmethod
    def get_valid_statuses() -> List[str]:
        """Returns a list of valid task status strings."""
        # We need to import the TaskStatus enum here to avoid circular imports
        # with the main app structure loading Config early.
        try:
            from app.models import TaskStatus
            return [s.value for s in TaskStatus]
        except ImportError:
            # Fallback in case models haven't fully initialized yet (e.g., during testing)
            return ["todo", "in_progress", "overdue", "done"]

# --- Initialization File ---
# app/utils/__init__.py
# (This file can be empty, but is necessary for Python to recognize the directory as a package)
