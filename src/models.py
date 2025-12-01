from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from src.api.users.users_models import UserOrm
from src.api.project.project_models import ProjectOrm
from src.api.task.task_models import TaskOrm

__all__ = [
    "Base",
    "UserOrm",
    "ProjectOrm",
    "TaskOrm"
]