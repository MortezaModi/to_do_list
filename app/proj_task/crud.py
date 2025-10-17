from .projects import Projects
from .tasks import tasks
from config import MAX_PROJECTS, MAX_TASKS
from datetime import datetime

class manager:
    def __init__(self):
        self.projects: list[Projects] = []

    def create_project(self, title: str,description: str = "" ):
        if len(title.split()) > 35:
            raise ValueError("Title is longer than 35 words")
        if len(description.split()) > 150:
            raise ValueError("Description is longer than 150 words")
        if any(p.title == title for p in self.projects):
            raise ValueError("Title already exists")
        if len(self.projects) >= MAX_PROJECTS:
            raise ValueError("NO MORE PROJECTS ALLOWED TO BE MADE")

    project = Projects(id=len(self.projects)+1, title=title, description=description)
    self.projects.append(project)
    return project

