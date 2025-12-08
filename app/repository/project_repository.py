from app.repository.base import *
from app.models import Project
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

class ProjectRepository(BaseRepository[Project, dict, dict]):
    """
    Repository for Project model. it inherits all basic CRUD operations from BaseRepository
    """
    def __init__(self, db: Session):
        super().__init__(Project, db)

    # Custom methods

    def get_by_title(self, title: str) -> Optional[Project]:
        # Retrieve by title
        from sqlalchemy import select
        stmt = select(self.model).where(self.model.title == title)
        return self.db.execute(stmt).scalars().first()

    def search(self, query: str, limit: int = 10) -> List[Project]:

        search_like = f'%{query}%'
        stmt = (
            select(self.model)
            .where(
                or_(
                    self.model.title.like(search_like),
                    self.model.description.like(search_like)
                )
            )
        )
        return list(self.db.execute(stmt).scalars().all())