from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services import TaskService
from app.api.schemas import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    HTTPError
)
from app.models import TaskStatus
from app.exceptions import AppException as TodoListException

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    # Define common responses for documentation
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPError, "description": "Resource not found"},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPError, "description": "Validation or business logic error"},
    },
)


# --- 1. GET All Tasks for a Project ---
@router.get(
    "/project/{project_id}",
    response_model=List[Task],
    summary="Retrieve All Tasks for a Project (Optionally filtered by Status)",
)
def get_tasks_for_project_endpoint(
        project_id: int,
        status_filter: TaskStatus = None,  # Optional query parameter for filtering
        db: Session = Depends(get_db)
):
    """
    Fetches a list of tasks belonging to a specific project.
    Can be optionally filtered by task status (e.g., ?status_filter=done).
    """
    service = TaskService(db)
    try:
        tasks = service.get_tasks_for_project(
            project_id=project_id,
            status=status_filter
        )
        return tasks
    except TodoListException as e:
        # Catches exceptions like "Project not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# --- 2. POST (Create) a New Task ---
@router.post(
    "/{project_id}/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Task in a Project",
)
def create_task_endpoint(
        project_id: int,
        task_data: TaskCreate,
        db: Session = Depends(get_db)
):
    """Creates a new task associated with the given project ID."""
    try:
        service = TaskService(db)
        task = service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            status=task_data.status
        )
        return task
    except TodoListException as e:
        # Catches validation errors or "Project not found"
        status_code = status.HTTP_404_NOT_FOUND if "Project not found" in str(e) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(e))


# --- 3. GET Single Task by ID ---
@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Retrieve Single Task by ID",
)
def get_task_by_id_endpoint(task_id: int, db: Session = Depends(get_db)):
    """Fetches a single task by its unique ID."""
    service = TaskService(db)
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task


# --- 4. PATCH (Update Details) ---
@router.patch(
    "/{task_id}",
    response_model=Task,
    summary="Update Task Details (Title, Description, Due Date)",
)
def update_task_details_endpoint(
        task_id: int,
        update_data: TaskUpdate,
        db: Session = Depends(get_db)
):
    """Updates the title, description, or due date of an existing task."""
    # Convert Pydantic model to a dictionary, ignoring unset values
    update_data_dict = update_data.model_dump(exclude_none=True, exclude_unset=True)

    if not update_data_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update.")

    try:
        service = TaskService(db)
        updated_task = service.update_task_details(task_id, **update_data_dict)
        return updated_task
    except TodoListException as e:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(e))


# --- 5. PATCH (Update Status) - Dedicated Endpoint for Business Rules ---
@router.patch(
    "/{task_id}/status",
    response_model=Task,
    summary="Update Task Status (e.g., todo -> doing -> done)",
)
def update_task_status_endpoint(
        task_id: int,
        status_update: TaskStatusUpdate,
        db: Session = Depends(get_db)
):
    """Updates only the status of a task, ensuring proper state transitions."""
    try:
        service = TaskService(db)

        # Check if the desired status is 'done' to use the specific service method
        if status_update.status == TaskStatus.DONE:
            updated_task = service.mark_task_as_done(task_id)
        else:
            # Use generic status update for other transitions (TODO, DOING, etc.)
            updated_task = service.update_task_status(task_id, status_update.status)

        return updated_task
    except TodoListException as e:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(e))


# --- 6. DELETE a Task ---
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Task",
)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    """Permanently deletes a task by ID."""
    try:
        service = TaskService(db)
        service.delete_task(task_id)
        return  # FastAPI will handle 204 No Content
    except TodoListException as e:
        # Catches if the task was not found prior to deletion
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
