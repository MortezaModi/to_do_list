from app.exceptions.base import AppException

from .repository_exceptions import (
    RepositoryException,
    TaskNotFoundException,
    ProjectNotFoundException,
    DuplicateRecordException,
    IntegrityError,
)

from .service_exceptions import (
    ServiceException,
    TaskAlreadyDoneException,
    InvalidTaskTransitionException,
    ProjectHasActiveTaskException,
    InvalidStatusTransitionException
)