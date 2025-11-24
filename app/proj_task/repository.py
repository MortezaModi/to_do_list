from .project_task import Project, Task

class ProjectRepository:
    def __init__(self):
        self.projects: list[Project] = []

    def add_project(self, project: Project):
        self.projects.append(project)

    def get_all_projects(self):
        return self.projects

    def get_project(self, project_id: int):
        for p in self.projects:
            if p.id == project_id:
                return p
        return None

    def delete_project(self, project_id: int):
        before = len(self.projects)
        self.projects = [p for p in self.projects if p.id != project_id]
        return before != len(self.projects)

