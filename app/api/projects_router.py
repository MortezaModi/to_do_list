from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services import ProjectService
from app.api.schemas import Project, ProjectCreate, ProjectUpdate, HTTPError
# Assuming your custom exceptions are defined here:
from app.exceptions import AppException as TodoListException, DuplicateRecordException

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    # Define common error responses for documentation
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPError, "description": "Resource not found"},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPError, "description": "Validation or business logic error"},
    },
)


# --- 1. POST (Create) a New Project ---
@router.post(
    "/",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Project",
)
def create_project_endpoint(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """Creates a new project, enforcing title uniqueness and non-null constraints."""
    try:
        service = ProjectService(db)
        project = service.create_project(title=project_data.title, description=project_data.description)
        return project
    except DuplicateRecordException as e:
        # Catches the specific error for non-unique title (returns 409 Conflict is often better than 400)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except TodoListException as e:
        # Catches generic business logic errors (like title being null/empty)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# --- 2. GET (Retrieve All) Projects ---
@router.get(
    "/",
    response_model=List[Project],
    summary="Retrieve All Projects",
)
def get_all_projects_endpoint(db: Session = Depends(get_db)):
    """Fetches a list of all existing projects."""
    service = ProjectService(db)
    return service.get_all_projects()


# --- 3. GET (Retrieve Single) Project by ID ---
@router.get(
    "/{project_id}",
    response_model=Project,
    summary="Retrieve Project by ID",
)
def get_project_by_id_endpoint(project_id: int, db: Session = Depends(get_db)):
    """Fetches a single project by its unique ID."""
    service = ProjectService(db)
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {project_id} not found.")
    return project


# --- 4. PATCH (Update Details) ---
@router.patch(
    "/{project_id}",
    response_model=Project,
    summary="Update Project Details (Title, Description)",
)
def update_project_endpoint(
        project_id: int,
        update_data: ProjectUpdate,
        db: Session = Depends(get_db)
):
    """
    Updates the title or description of an existing project.
    Only fields provided in the body will be changed.
    """
    # Convert Pydantic model to a dictionary, ignoring unset values for PATCH
    update_data_dict = update_data.model_dump(exclude_none=True, exclude_unset=True)

    if not update_data_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update.")

    try:
        service = ProjectService(db)
        updated_project = service.update_project(project_id, **update_data_dict)
        return updated_project
    except TodoListException as e:
        # Catches errors like "Project not found" or "Title is not unique"
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(e))


# --- 5. DELETE (Remove) Project ---
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Project",
)
def delete_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    """
    Permanently deletes a project by ID.
    Note: The Service Layer must handle cascading deletion of related tasks.
    """
    try:
        service = ProjectService(db)
        service.delete_project(project_id)
        return  # FastAPI handles the 204 No Content response
    except TodoListException as e:
        # Catches if the project was not found prior to deletion
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
