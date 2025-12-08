from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services import ProjectService
from app.api.schemas import Project, ProjectCreate, ProjectUpdate, HTTPError
from app.exceptions import AppException as TodoListException
from typing import List

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPError}},
)

@router.post(
    "/",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Project",
)
def create_project_endpoint(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """Creates a new project with validation enforced by the Service Layer."""
    try:
        service = ProjectService(db)
        project = service.create_project(title=project_data.title, description=project_data.description)
        return project
    except TodoListException as e:
        # Catch business logic validation errors (e.g., title too long)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/",
    response_model=List[Project],
    summary="Retrieve All Projects",
)
def get_all_projects_endpoint(db: Session = Depends(get_db)):
    """Fetches a list of all existing projects."""
    service = ProjectService(db)
    return service.get_all_projects()

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return project

# ... (Implement PUT/PATCH and DELETE endpoints similarly, connecting them to ProjectService methods)