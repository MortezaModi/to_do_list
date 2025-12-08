from fastapi import FastAPI
from app.api import projects_router, tasks_router
from app.db import base # Ensures SQLAlchemy models are loaded

# Initialize the FastAPI application
app = FastAPI(
    title="ToDoList REST API",
    description="Full web service for managing projects and tasks. CLI is deprecated.",
    version="v1.0.0",
    redoc_url="/docs", # Standard documentation URL
)

# Include Routers for modular organization
app.include_router(projects_router.router, prefix="/v1")
app.include_router(tasks_router.router, prefix="/v1")

# The main function to run the API using Uvicorn (standard ASGI server)
def start_api():
    """Starts the FastAPI application using Uvicorn."""
    import uvicorn
    # Use 0.0.0.0 for external access; port 8000 is default
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_api()