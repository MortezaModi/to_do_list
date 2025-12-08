# main.py

import os
import sys
from dotenv import load_dotenv

from app.api.main import start_api

# --- 1. Environment and Base Setup ---

# Load environment variables (e.g., DATABASE_URL) from a .env file
load_dotenv()

# Import the Base for SQLAlchemy to ensure all models are registered with the Metadata.
# This is necessary before any database operations or migrations are run.
from app.db import base # noqa: F401

# -- WARNING --
def print_deprecation_warning():
    pass

# --- 2. Import and Run the CLI ---

# Import the main function that initializes and runs the menu-driven interface
from app.cli.console import main as cli_main


if __name__ == "__main__":
    # Execute the main entry point for the interactive CLI application.
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        print_deprecation_warning()
        cli_main()
    else:
        print("Startinh todolist REST API")
        print("Access documented at http://127.0.0.1:8000/docs")
        start_api()

