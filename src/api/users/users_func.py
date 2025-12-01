from fastapi import Depends,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth_config import oauth2_scheme
from src.api.auth.auth_crud import auth_crud
from src.api.auth.auth_func import auth_get_user_func, auth_check_role_user, get_user_role_from_token
from src.api.users.users_models import UserOrm, RoleEnum
from src.api.users.users_schema import UsersReturnSchema, UserSchema
from src.database import get_async_db


from src.api.users.users_exceptions import UserNotFoundException, ForbiddenException
from src.api.users.users_exceptions import UsersNotFoundException

from src.api.users.users_crud import user_crud

# -----------------------------
# Чистая логика, можно вызывать напрямую
# -----------------------------
async def get_users_logic(db: AsyncSession, token: str):
    """
    Получение всех пользователей с проверкой роли.
    Выбрасывается ForbiddenException если у пользователя нет прав.
    """
    user_role = await get_user_role_from_token(token, db)
    if user_role == RoleEnum.user:
        raise ForbiddenException()

    # Здесь логика получения всех пользователей
    users = await auth_crud.get_all_users(db=db)
    return users


# -----------------------------
# Функция для использования с Depends в роутере
# -----------------------------
async def get_users_db(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    return await get_users_logic(db=db, token=token)

# Для получения одного пользователя
async def get_one_user_by_id_db(
    name: str,
    db: AsyncSession = Depends(get_async_db),
    token: str = Depends(oauth2_scheme),
):
    user_orm = await user_crud.get_by_name(db,name)

    if not user_orm:
        # Вызываеам кастомную ошибку на отсутствие пользователя в БД
        raise UserNotFoundException(name)

    return UserSchema(name=user_orm.name)