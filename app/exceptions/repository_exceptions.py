from pyexpat.errors import messages
from typing import Optional
from app.exceptions.base import AppException

class RepositoryException(AppException):
    """base exception for all repository-related exceptions"""
    pass

class ProjectNotFoundException(RepositoryException):
    """exception raised for not finding a project in the db"""
    def __init__(self, message:str = "Project not found", project_id: Optional[int] = None):
        if project_id is not None:
            message = f"Project with id {project_id} not found"
        super().__init__(message)

class TaskNotFoundException(RepositoryException):
    """exception raised for not finding a task in the db"""
    def __init__(self, message:str = "Task not found", task_id: Optional[int] = None):
        if task_id is not None:
            message = f"task with id {task_id} not found"
        super().__init__(message)


class DuplicateRecordException(RepositoryException):
    """exception raised for duplicate records"""
    def __init__(self, model_name: str, field: str, value: str):
        message = f"Can not create {model_name} : A record with the same {field}'{value}' already exists"
        super().__init__(message)

class IntegrityError(RepositoryException):
    """
    raised for generic integrity errors like FK violations though
    these are handled as Duplicate records or just not found
    """
    def __init__(self, message: str = "Database integrity violation occurred"):
        super().__init__(message)