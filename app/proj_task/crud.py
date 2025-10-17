from .project_task import Project, Task
from config import MAX_PROJECTS, MAX_TASKS, VALID_STATUSES
from datetime import datetime

class manager:
    def __init__(self):
        self.projects: list[Project] = []

    def create_project(self, name: str, description: str = "" ):
        if len(name.split()) > 35:
            raise ValueError("Title is longer than 35 words")
        if len(description.split()) > 150:
            raise ValueError("Description is longer than 150 words")
        if any(p.name == name for p in self.projects):
            raise ValueError("Title already exists")
        if len(self.projects) >= MAX_PROJECTS:
            raise ValueError("NO MORE PROJECTS ALLOWED TO BE MADE")

        project = Project(id=len(self.projects) + 1, name=name, description=description)
        self.projects.append(project)
        return project


    def list_projects(self):
            return self.projects

    def update_project(self, project_id: int, title: str, description: str):
        for p in self.projects:
            if p.id == project_id:
                if any(x.title == title and x.id != project_id for x in self.project):
                    raise ValueError("PROJECT ALREADY EXISTS")
                p.title = title
                p.description = description
                return p
        raise ValueError("PROJECT NOT FOUND 404")

    def delete_project(self, project_id: int):
        before_count = len(self.projects)
        self.projects = [p for p in self.projects if p.id != project_id]
        after_count = len(self.projects)
        if before_count == after_count:
            raise ValueError("PROJECT NOT FOUND")
        return True  # Cascade delete happens automatically since tasks are inside project

    # -------- TASKS -------- #
    def create_task(self, project_id: int, title: str, description: str = "", deadline=None):
        project = self._get_project(project_id)
        if len(project.tasks) >= MAX_TASKS:
            raise ValueError("TOO MANY TASKS")
        if len(title.split()) > 30:
            raise ValueError("TITLE is longer than 30 words")
        if len(description.split()) > 150:
            raise ValueError("DESCRIPTION is longer than 150 words")
        if deadline and not isinstance(deadline, datetime):
            raise ValueError("INVALID DEADLINE")

        task = Task(id=len(project.tasks) + 1, title=title, description=description)
        project.tasks.append(task)
        return task

    def list_tasks(self, project_id: int):
        project = self._get_project(project_id)
        return project.tasks

    def update_task(self, project_id: int, task_id: int, **kwargs):
        project = self._get_project(project_id)
        task = self._get_task(project, task_id)
        for key, value in kwargs.items():
            if key == "status" and value not in VALID_STATUSES:
                raise ValueError("INVALID STATUS")
            if value is not None:
                setattr(task, key, value)
        return task

    def delete_task(self, project_id: int, task_id: int):
        project = self._get_project(project_id)
        before = len(project.tasks)
        project.tasks = [t for t in project.tasks if t.id != task_id]
        if before == len(project.tasks):
            raise ValueError("TASK NOT FOUND")
        return True

        # -------- HELPERS -------- #
    def _get_project(self, project_id: int) -> Project:
        for p in self.projects:
            if p.id == project_id:
                return p
        raise ValueError("PROJECT NOT FOUND")

    def _get_task(self, project: Project, task_id: int) -> Task:
        for t in project.tasks:
            if t.id == task_id:
                return t
        raise ValueError("TASK NOT FOUND")




