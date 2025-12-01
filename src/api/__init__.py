from fastapi import APIRouter

from src.api.db.db import db as db_router
from src.api.users.users_router import users as users_router
from src.api.auth.auth_router import auth as auth_router
from src.api.project.project_router import project as project_router
from src.api.task.task_router import task as task_router

main_router = APIRouter()

main_router.include_router(db_router)
main_router.include_router(users_router)
main_router.include_router(auth_router)
main_router.include_router(project_router)
main_router.include_router(task_router)