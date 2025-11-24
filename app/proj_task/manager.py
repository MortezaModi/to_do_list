from datetime import datetime
from app.proj_task.config import MAX_PROJECTS, MAX_TASKS, VALID_STATUSES
from .project_task import Project, Task
from .repository import ProjectRepository


class Manager:
    def __init__(self, repository: ProjectRepository):
        self.repo = repository

    # -------- PROJECTS -------- #
    def create_project(self, name: str, description: str = ""):
        # --- Business Logic ---
        if len(name.split()) > 35:
            raise ValueError("Title is longer than 35 words")
        if len(description.split()) > 150:
            raise ValueError("Description is longer than 150 words")
        if any(p.name == name for p in self.repo.get_all_projects()):
            raise ValueError("Title already exists")
        if len(self.repo.get_all_projects()) >= MAX_PROJECTS:
            raise ValueError("No more projects allowed")

        project = Project(
            id=len(self.repo.get_all_projects()) + 1,
            name=name,
            description=description
        )

        self.repo.add_project(project)
        return project

    def list_projects(self):
        return self.repo.get_all_projects()

    def update_project(self, project_id: int, name: str, description: str):
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("PROJECT NOT FOUND")

        if any(p.name == name and p.id != project_id for p in self.repo.get_all_projects()):
            raise ValueError("PROJECT ALREADY EXISTS")

        project.name = name
        project.description = description
        return project

    def delete_project(self, project_id: int):
        success = self.repo.delete_project(project_id)
        if not success:
            raise ValueError("PROJECT NOT FOUND")
        return True

    # -------- TASKS -------- #
    def create_task(self, project_id: int, title: str, description: str = "", deadline=None):
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("PROJECT NOT FOUND")

        # business logic
        if len(project.tasks) >= MAX_TASKS:
            raise ValueError("TOO MANY TASKS")
        if len(title.split()) > 30:
            raise ValueError("TITLE longer than 30 words")
        if len(description.split()) > 150:
            raise ValueError("DESCRIPTION longer than 150 words")
        if deadline and not isinstance(deadline, datetime):
            raise ValueError("INVALID DEADLINE")

        task = Task(id=len(project.tasks) + 1, title=title, description=description)
        project.tasks.append(task)
        return task

    def list_tasks(self, project_id: int):
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("PROJECT NOT FOUND")
        return project.tasks

    def update_task(self, project_id: int, task_id: int, **kwargs):
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("PROJECT NOT FOUND")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("TASK NOT FOUND")

        for key, value in kwargs.items():
            if key == "status" and value not in VALID_STATUSES:
                raise ValueError("INVALID STATUS")
            setattr(task, key, value)

        return task

    def delete_task(self, project_id: int, task_id: int):
        project = self.repo.get_project(project_id)
        if not project:
            raise ValueError("PROJECT NOT FOUND")

        before = len(project.tasks)
        project.tasks = [t for t in project.tasks if t.id != task_id]

        if before == len(project.tasks):
            raise ValueError("TASK NOT FOUND")
        return True

