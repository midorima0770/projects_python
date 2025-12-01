from fastapi import status

from src.exceptions import AppException

class TasksNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message=f"Tasks not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class TaskNotFoundException(AppException):
    def __init__(self,id: int):
        super().__init__(
            message=f"Task with id = {id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class TaskAlreadyExistsException(AppException):

    def __init__(self,title,assignee_id):
        super().__init__(
            message=f"Task with title = {title} , and owner_id = {assignee_id} is already",
            status_code=status.HTTP_409_CONFLICT
        )

class TaskAccessForbiddenException(AppException):
    def __init__(self):
        super().__init__(
            message=f"You do not have permission to access this task.",
            status_code=status.HTTP_403_FORBIDDEN
        )

class DeadlineExceededException(AppException):
    def __init__(self):
        super().__init__(
            message=f"The task's deadline has already passed, you cannot change the task's status.",
            status_code=status.HTTP_403_FORBIDDEN
        )

class InvalidStatusTransitionException(AppException):
    def __init__(self):
        super().__init__(
            message=f"You cannot change the status from todo to done",
            status_code=status.HTTP_409_CONFLICT
        )

class InvalidStatusTransitionInProgressException(AppException):
    def __init__(self):
        super().__init__(
            message=f"You cannot change the status from done to in_progress",
            status_code=status.HTTP_409_CONFLICT
        )

class DeadlinePassed(AppException):
    def __init__(self):
        super().__init__(
            message=f"The deadline has passed.",
            status_code=status.HTTP_403_FORBIDDEN
        )