import enum
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from app.db.base import Base

class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING ="doing"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.TODO, # default set it to "todo"
        nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)


    # relation with project
    project = relationship("Project", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task (id={self.id}, title='{self.title}', status='{self.status.value}', project_id={self.project_id})>"
