from datetime import datetime
from typing import List, Optional


class Project:
    def __init__(self, id: int, name: str, description: str = ""):
        self.id = id
        self.name = name
        self.description = description
        self.tasks: list[Task] = []


    def __repr__(self):
            return f"Project(id={self.id}, name='{self.name}')"

    def __str__(self):
            return f" {self.id}. {self.name} — {self.description}"


class Task:
    def __init__(self, id: int, title: str, description: str = "", status: str = "todo", deadline: datetime | None = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"

    def __str__(self):
        if self.deadline :
            deadline_str = self.deadline.strftime("%Y-%m-%d")
        return f"📝 {self.id}. {self.title} — {self.status} ({deadline_str})"

