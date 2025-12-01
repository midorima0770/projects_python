from fastapi import status

from src.exceptions import AppException

class UsersNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message=f"Users not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class UserNotFoundException(AppException):
    def __init__(self, user_name: str | None = None):
        super().__init__(
            message=f"User with name={user_name} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ForbiddenException(AppException):
    def __init__(self):
        super().__init__(
            message=f"You do not have permission to perform this action",
            status_code=status.HTTP_403_FORBIDDEN
        )