from fastapi import status

from src.exceptions import AppException

class ProjectsNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message=f"Projects not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ProjectNotFoundException(AppException):
    def __init__(self, id):
        super().__init__(
            message=f"Project with id = {id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ProjectAlreadyExistsException(AppException):

    def __init__(self,title,owner_id):
        super().__init__(
            message=f"Project with title = {title} , and owner_id = {owner_id} is already",
            status_code=status.HTTP_409_CONFLICT
        )

class ProjectAccessForbiddenException(AppException):
    def __init__(self):
        super().__init__(
            message=f"You do not have permission to access this project.",
            status_code=status.HTTP_403_FORBIDDEN
        )