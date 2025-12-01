from fastapi import status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.auth.security import hash_password
from src.api.db.base_crud import BaseCRUD
from src.api.users.users_models import UserOrm, RoleEnum


# CRUD auth
class AuthBaseCrud(BaseCRUD):

    model=UserOrm

    # Для создания админа
    async def create_admin(self,db: AsyncSession,name,password):
        user_orm = UserOrm(
            name=name,
            password=hash_password(password),
            role=RoleEnum.admin
        )
        db.add(user_orm)
        await db.commit()

    # Для проверки дубликата имени
    async def check_user_is_already(self,db: AsyncSession,name):
        result = await db.execute(select(self.model).where(
            self.model.name == name
        ))
        return result.scalars().one_or_none()

    # Регистрация
    async def register_user(self,db: AsyncSession,name: str,password: str):
        user_orm = UserOrm(
            name=name,
            password=password,
            role=RoleEnum.user
        )
        db.add(user_orm)
        await db.commit()

    async def get_user_crud(self, db: AsyncSession, id: int):
        result = await db.execute(
            select(UserOrm)
            .options(selectinload(UserOrm.projects))  # предзагрузка проектов
            .where(UserOrm.id == id)
        )
        return result.scalars().one_or_none()

    async def get_all_users(self,db: AsyncSession):
        result = await db.execute(select(UserOrm).options(selectinload(UserOrm.projects)))
        users_orm = result.scalars().all()

        if users_orm:
            return users_orm
        else:
            return None

auth_crud = AuthBaseCrud(UserOrm)