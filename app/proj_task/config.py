import os
from dotenv import load_dotenv

load_dotenv()

MAX_PROJECTS = int(os.getenv("MAX_PROJECTS", 10))
MAX_TASKS = int(os.getenv("MAX_TASKS", 50))
VALID_STATUSES = {"todo", "doing", "done"}