"""Base repository with generic CRUD operations."""

from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, and_, or_

T = TypeVar('T')


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def create(self, **kwargs: Any) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_by_id(self, id: int) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = self.db.execute(stmt)
        return list(result.scalars().all())

    def get_by_filters(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[T]:
        stmt = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        stmt = stmt.offset(skip).limit(limit)
        result = self.db.execute(stmt)
        return list(result.scalars().all())

    def update(self, id: int, **kwargs: Any) -> Optional[T]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        stmt = select(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
        result = self.db.execute(stmt)
        return len(list(result.scalars().all()))

    def bulk_create(self, items: List[Dict[str, Any]]) -> List[T]:
        instances = [self.model(**item) for item in items]
        self.db.add_all(instances)
        self.db.commit()
        for instance in instances:
            self.db.refresh(instance)
        return instances
