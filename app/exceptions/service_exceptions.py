from pyexpat.errors import messages

from app.exceptions.base import AppException

class ServiceException(AppException):
    pass

class TaskAlreadyDoneException(ServiceException):

    def __init__(self, task_id: int):
        message = f"Task ID {task_id} is already marked as DONE"
        super().__init__(message)

class InvalidTaskTransitionException(ServiceException):
    """raised when an invalid status change is attempted like from todo to done with out doing"""
    def __init__(self, current_status: str, new_status: str):
        message = f"Invalid status transition from '{current_status}' to '{new_status}'"
        super().__init__(message)

class ProjectHasActiveTaskException(ServiceException):
    def __init__(self, project_id: int, active_count: int):
        message = f"Project ID {project_id} has {active_count} active tasks, so it cannot be deleted"
        super().__init__(message)

class InvalidStatusTransitionException(ServiceException):
    def __init__(self, task_id: int, current_status: str, new_status: str):
        message = (
            f"Task ID {task_id}: Invalid status transition attempted"
            f"from '{current_status}' to '{new_status}'."
        )
        super().__init__(message)

