from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth_config import oauth2_scheme
from src.api.users.users_exceptions import UserNotFoundException
from src.database import get_async_db

from src.api.users.users_func import get_users_db
from src.api.users.users_func import get_one_user_by_id_db

users = APIRouter(tags=["users"],prefix="/users")

@users.get("/get/all")
async def get_users(
    users=Depends(get_users_db)  # FastAPI сам передаст token и db
):
    return users

@users.get("/get/{name}")
async def get_user_by_name(
    name: str,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await get_one_user_by_id_db(name, db)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with name={name} not found")