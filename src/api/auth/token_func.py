from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from src.config import settings

# Создание токенов
def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict) -> str:
    return create_token(data, timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)))

def create_refresh_token(data: dict) -> str:
    return create_token(data, timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_DAYS)))


# Проверка и декодирование токена
def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None