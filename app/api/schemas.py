from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from app.models import TaskStatus  # Enum from your models


# --- Utility Schema ---
class HTTPError(BaseModel):
    """Schema for standard API error responses."""
    detail: str = Field(..., description="Details of the error encountered.")


# --- Project Schemas ---
class ProjectBase(BaseModel):
    """Shared properties for project creation and updates."""
    title: str = Field(..., min_length=1, max_length=50,
                       description="Project title (1-5 words limit enforced by Service Layer).")
    description: Optional[str] = Field(None, max_length=100, description="Optional project description.")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(ProjectBase):
    """Schema for updating an existing project (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=100)


class Project(ProjectBase):
    """Full project schema (used for responses)."""
    id: int
    created_at: datetime
    updated_at: datetime

    # We won't include 'tasks' in the main Project response to prevent circular dependencies/heavy payloads

    class Config:
        # Allows conversion from SQLAlchemy models (ORM mode)
        from_attributes = True


# --- Task Schemas ---
class TaskBase(BaseModel):
    """Shared properties for task creation and updates."""
    title: str = Field(..., min_length=1, max_length=80, description="Task title.")
    description: Optional[str] = Field(None, max_length=300, description="Task description.")
    due_date: Optional[date] = Field(None, description="Optional deadline in YYYY-MM-DD format.")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    status: TaskStatus = Field(TaskStatus.TODO, description="Initial status of the task.")
    # project_id is passed via the path/URL, not the body, but included here for clarity


class TaskUpdate(TaskBase):
    """Schema for updating task details (excluding status)."""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None


class TaskStatusUpdate(BaseModel):
    """Schema for updating only the task status."""
    status: TaskStatus


class Task(TaskBase):
    """Full task schema (used for responses)."""
    id: int
    project_id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True