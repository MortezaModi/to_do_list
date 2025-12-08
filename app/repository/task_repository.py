from app.repository.base import *
from app.models import Task, TaskStatus
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func

class TaskRepository(BaseRepository[Task, dict, dict]):
    """
    Repository for interacting with tasks
    """
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_tasks_by_project(self, project_id: int, status: Optional[TaskStatus] = None) -> List[Task]:
        condition = [self.model.project_id == project_id]

        if status:
            condition.append(self.model.status == status)

        stmt = select(self.model).where(and_(*condition)).order_by(self.model.created_at)
        return list(self.db.execute(stmt).scalars().all())

    def update_status(self, task_id: int, new_status: TaskStatus) -> Optional[Task]:
        # quickly update the status
         return self.update(task_id, {'status': new_status})

    def mark_as_done(self, task_id: int) -> Optional[Task]:

        from app.models import TaskStatus

        return self.update_status(task_id, TaskStatus.DONE)

    def get_task_count(self, project_id: int) -> int:

        stmt = select(func.count(self.model.id)).where(self.model.project_id == project_id)
        return self.db.execute(stmt).scalar_one()