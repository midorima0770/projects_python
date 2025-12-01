from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.db.base_crud import BaseCRUD
from src.api.users.users_models import UserOrm


class UserBaseCrud(BaseCRUD):

    model=UserOrm

    async def get_by_name(self,db: AsyncSession,name):
        result = await db.execute(select(self.model).where(
            self.model.name == name
        ))
        return result.scalars().one_or_none()

user_crud = UserBaseCrud(UserOrm)