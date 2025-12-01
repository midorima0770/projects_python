from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth_config import oauth2_scheme
from src.api.auth.auth_exceptions import InvalidCredentialsLoginException, InvalidRefreshTokenException, \
    InvalidTokenException, UserAlreadyExistsException
from src.api.auth.auth_func import auth_func_register, login, refresh_token_func, get_me_func
from src.database import get_async_db

from src.api.auth.auth_schema import RegisterSchema, Token
from src.exceptions import logger

auth = APIRouter(prefix="/auth",tags=["auth"])



# Роутер на регистрацию
@auth.post("/register")
async def auth_register(
    register_schema: RegisterSchema,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await auth_func_register(name=register_schema.name,password=register_schema.password,db=db)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with name{register_schema.name} is already")
    except Exception as e:
        logger.exception(e)

# Роутер на вход
@auth.post("/login", response_model=Token)
async def auth_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await login(form_data=form_data,db=db)
    except InvalidCredentialsLoginException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"User with name={form_data.username} is not already or password is not correct")
    except Exception as e:
        logger.exception(e)

# Роутер на обновление токена
@auth.post("/refresh", response_model=Token)
async def auth_refresh_token(
    refresh_token: str
):
    try:
        return await refresh_token_func(refresh_token)
    except InvalidRefreshTokenException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid refresh token")
    except Exception as e:
        logger.exception(e)

@auth.get("/me")
async def get_me(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await get_me_func(token=token,db=db)
    except InvalidTokenException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    except Exception as e:
        logger.exception(e)