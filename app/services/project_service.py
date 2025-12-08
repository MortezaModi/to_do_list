from typing import List, Optional

from sqlalchemy.orm import Session
from app.models import Project, TaskStatus
from app.repository import ProjectRepository, TaskRepository
from app.exceptions import (
    ProjectNotFoundException,
    DuplicateRecordException,
    ProjectHasActiveTaskException
)

class ProjectService:
    # business logic for project

    def __init__(self, db: Session):
        self.project_repo = ProjectRepository(db)
        self.task_repo = TaskRepository(db)

    def create_project(self, title:str, description: Optional[str] = None) ->Project:
        """
        Creates a new project after ensuring that the project title is unique
        """
        # business rule 1 : project title must be unique
        existing_project = self.project_repo.get_by_title(title)
        if existing_project:
            raise DuplicateRecordException(f"Project with title '{title}' already exists")

        # repository call to create
        project_data = {"title": title, "description": description}
        new_project = self.project_repo.create(project_data)

        return new_project

    #read
    def get_project_by_id(self, project_id: int) -> Project:
        """
        retrive a project by its id
        """
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(f"Project with id '{project_id}' not found")
        return project

    def get_all_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """retrieve all projects"""
        return self.project_repo.get_all(skip=skip, limit=limit)

    # update
    def update_project(self, project_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Project:
        """updates a project. including unique check for the new title"""
        self.get_project_by_id(project_id) # check existence

        # business rule 2 : check for duplicate title

        if title:
            existing_project = self.project_repo.get_by_title(title)
            # ensure the title belong to a dif project
            if existing_project and existing_project.id != project_id:
                raise DuplicateRecordException(f"Project with title '{title}' already exists")

        update_data = {}
        if title is not None :
            update_data["title"] = title
        if description is not None :
            update_data["description"] = description

        updated_project = self.project_repo.update(project_id, update_data)
        return updated_project

    # delete
    def delete_project(self, project_id: int) -> Project:
        project = self.get_project_by_id(project_id)

        # business rule3 : cannot delete project if it has active tasks
        active_tasks = self.task_repo.get_task_by_project(project_id, status=TaskStatus.TODO)
        active_tasks.extend(self.task_repo.get_task_by_project(project_id, status=TaskStatus.DOING))

        if active_tasks:
            raise ProjectHasActiveTaskException(project_id=project_id, active_count=len(active_tasks))

        deleted_project = self.project_repo.delete(project_id)
        return deleted_project

    def search_projects(self, query: str) -> List[Project]:
        return self.project_repo.search_by_fields(query, fields=["title", "description"])


