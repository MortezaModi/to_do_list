from typing import Generic, TypeVar, Type, Optional, List, Any, Dict

from sqlalchemy.orm import Session
from sqlalchemy import select, or_ , String #, update as sql_update, delete as sql_delete
from app.db.base import Base

# defining type vars for generic typing
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    # this is base class for all repositories ,providing common CRUD operation!

    def __init__(self, model: Type[ModelType], db: Session):

        self.model = model
        self.db = db

    # read operators
    def get_by_id(self, id: int) -> Optional[ModelType]:
        # Retrieve a record by PK (id)
        stmt = select(self.model).where(self.model.id == id)
        return self.db.execute(stmt).scalars().first()

    def get_all(self, skip: int=0, limit: int=100) -> List[ModelType]:
        # retrieve all records with optional pagination
        stmt = select(self.model).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    # Create operation

    def create(self, obj_in: Dict[str, Any] | CreateSchemaType) -> ModelType:
        # create a new record
        if hasattr(obj_in, "dict"):
            obj_in_data = obj_in.dict(exclude_unset=True)
        else:
            obj_in_data = obj_in

        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    # update operation
    def update(self, id: Any, obj_in: Dict[str, Any] | UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        if hasattr(obj_in, "dict"):
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = obj_in

        for key, value in update_data.items():
            if value is not None:
                setattr(db_obj, key, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    # delete operation

    def delete(self, id: Any) -> Optional[ModelType]:
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj # return deleted obj or None

    def search_by_fields(self, search_query: str, fields: List[str], project_id: Optional[int]=None) -> List[ModelType]:

        search_terms =[
            getattr(self.model, field).ilike(f"%{search_query}%")
            for field in fields
        ]

        stmt = select(self.model).where(or_(*search_terms))

        if project_id is not None and hasattr(self.model, "project_id"):
            stmt = stmt.where(self.model.project_id == project_id)

        return list(self.db.execute(stmt).scalars().all())