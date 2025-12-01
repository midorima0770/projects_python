from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

ModelType = TypeVar("ModelType")

class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, obj_id: int):
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalars().one_or_none()
