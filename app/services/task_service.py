from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select, and_

# Import Models and Enums
from app.models import Task, TaskStatus
# Import Repositories
from app.repository import TaskRepository, ProjectRepository
# Import Custom Exceptions
from app.exceptions import (
    TaskNotFoundException,
    ProjectNotFoundException,
    InvalidStatusTransitionException
)


class TaskService:
    """
    Handles the business logic for Task operations, focusing on project dependency
    and task status transitions.
    """

    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    # --- CREATE ---
    def create_task(self, project_id: int, title: str, description: Optional[str] = None, due_date=None, status: str = "TODO") -> Task:
        """
        Creates a new task associated with an existing project.
        """
        # Business Rule 1: Ensure the project exists before creating the task
        if not self.project_repo.get_by_id(project_id):
            raise ProjectNotFoundException(f"Project ID {project_id}")

        # Repository call to create the record (status defaults to TODO in the model)
        task_data = {
            "project_id": project_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "status": status
        }
        new_task = self.task_repo.create(task_data)
        return new_task

    # --- READ ---
    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieves a task by ID or raises an exception if not found.
        """
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(f"Task ID {task_id}")
        return task

    def get_tasks_for_project(self, project_id: int, status: Optional[TaskStatus] = None) -> List[Task]:
        """
        Retrieves all tasks for a given project, optionally filtered by status.
        """
        # Optional: Check if the project exists, though the repository handles the query
        if not self.project_repo.get_by_id(project_id):
            raise ProjectNotFoundException(f"Project ID {project_id}")

        return self.task_repo.get_tasks_by_project(project_id, status)

    # --- UPDATE ---
    def update_task_details(self, task_id: int, **kwargs) -> Task:
        """
        Updates fields like title, description, or due_date.
        """
        self.get_task_by_id(task_id)  # Ensure task exists

        # We pass kwargs directly to the repository update method
        updated_task = self.task_repo.update(task_id, kwargs)
        return updated_task

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        """
        Handles the business logic for changing a task's status.
        """
        task = self.get_task_by_id(task_id)

        # Business Rule 2: Basic Status Transition Check
        current_status = task.status

        # Prevent jumping straight to DONE from TODO (optional complexity)
        # if current_status == TaskStatus.TODO and new_status == TaskStatus.DONE:
        #     raise InvalidStatusTransitionException(...)

        # Prevent setting a status to the current status (optimization, not a rule)
        if current_status == new_status:
            return task

        # Update the status via the repository
        updated_task = self.task_repo.update_status(task_id, new_status)
        return updated_task

    def mark_task_as_done(self, task_id: int) -> Task:
        """
        Helper method to apply the specific transition to DONE.
        """
        task = self.get_task_by_id(task_id)
        if task.status == TaskStatus.DONE:
            # Although the generic update would just refresh the object,
            # we explicitly use a business rule violation if needed later.
            return task

        return self.update_task_status(task_id, TaskStatus.DONE)

    # --- DELETE ---
    def delete_task(self, task_id: int) -> Task:
        """
        Deletes a task record.
        """
        self.get_task_by_id(task_id)  # Ensures task exists
        deleted_task = self.task_repo.delete(task_id)
        return deleted_task

    def get_task_count(self, project_id: int) -> int:

        return self.task_repo.get_task_count(project_id)

    def search_tasks(self, project_id: int, query: str) -> List[Task]:

        return self.task_repo.search_by_fields(query, fields=["title", "description", "due_date"])



    def autoclose_overdue_tasks(self) -> int:
        """
        Finds tasks that are past their due_date and not DONE, and marks them as DONE.
        """
        today = datetime.today()
        updated_count = 0

        # 1. Find overdue tasks using a direct SQLAlchemy query
        stmt = (
            select(Task)
            .where(
                and_(
                    Task.due_date != None,
                    Task.due_date < today,
                    Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
                )
            )
        )

        overdue_tasks = self.task_repo.db.execute(stmt).scalars().all()

        # 2. Update each task status
        for task in overdue_tasks:
            # We bypass the complex transition logic here
            # since a cron job is often an exception to normal user workflow.
            # If business rules are critical, use update_task_status,
            # but usually, batch updates are simpler/faster.
            self.task_repo.update_status(task.id, TaskStatus.DONE)
            updated_count += 1

        return updated_count

