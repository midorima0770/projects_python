from fastapi import status

from src.exceptions import AppException

class UserAlreadyExistsException(AppException):
    def __init__(self,name):
        super().__init__(
            message=f"User with name{name} is already",
            status_code=status.HTTP_409_CONFLICT
        )

class InvalidCredentialsLoginException(AppException):
    def __init__(self,name):
        super().__init__(
            message=f"User with name={name} is not already or password is not correct",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class InvalidRefreshTokenException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid refresh token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )