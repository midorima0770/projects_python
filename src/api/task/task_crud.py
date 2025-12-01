from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.db.base_crud import BaseCRUD
from src.api.task.task_exceptions import DeadlineExceededException, TaskNotFoundException
from src.api.task.task_models import TaskOrm, TaskStatusEnum
from src.api.task.task_schema import CreateTaskSchema
from fastapi import status
from sqlalchemy import func

from zoneinfo import ZoneInfo

from src.api.users.users_models import UserOrm, RoleEnum


class TaskBaseCrud(BaseCRUD):

    model=TaskOrm

    async def get_all_tasks(self,db: AsyncSession,user: UserOrm):
        if user.role == RoleEnum.user:
            result = await db.execute(select(TaskOrm)
            .options(selectinload(TaskOrm.project))
            .where(
                TaskOrm.assignee_id == user.id
            ))
            tasks = result.scalars().all()
            return tasks
        else:
            result = await db.execute(select(TaskOrm).options(selectinload(TaskOrm.project)))
            tasks = result.scalars().all()
            return tasks

    async def get_task_by_id(self,db: AsyncSession,id: int):
        result = await db.execute(select(TaskOrm).where(
            TaskOrm.id == id
        ))
        task = result.scalars().one_or_none()
        return task

    async def delete_task(self,db: AsyncSession,id: int):
        result = await db.execute(select(TaskOrm).where(
            TaskOrm.id == id
        ))
        task = result.scalars().one_or_none()
        if not task:
            return False
        await db.delete(task)
        await db.commit()
        return True


    async def check_task_is_already(self,db: AsyncSession,new_task: CreateTaskSchema):
        result = await db.execute(select(TaskOrm).where(
            TaskOrm.assignee_id == new_task.assignee_id,
            TaskOrm.project_id == new_task.project_id,
            func.lower(TaskOrm.title) == func.lower(new_task.title)
        ))
        task = result.scalars().one_or_none()
        return task

    async def create_task(self,db: AsyncSession,new_task: CreateTaskSchema):
        task_orm = TaskOrm(
            title=new_task.title,
            description=new_task.description,
            status=TaskStatusEnum.TODO,
            deadline=new_task.deadline,
            created_at=datetime.now(ZoneInfo("Europe/Moscow")),
            project_id=new_task.project_id,
            assignee_id=new_task.assignee_id
        )
        db.add(task_orm)
        await db.commit()

    async def change_status_without_new_status(self,db: AsyncSession,id: int):
        result = await db.execute(select(TaskOrm).where(
            TaskOrm.id==id
        ))
        task = result.scalars().one_or_none()
        if not task:
            return TaskNotFoundException(id)
        if task.deadline > datetime.now(ZoneInfo("Europe/Moscow")):

            if task.status == TaskStatusEnum.TODO:
                task.status = TaskStatusEnum.IN_PROGRESS
                await db.commit()
                return {"new_status": TaskStatusEnum.IN_PROGRESS}
            elif task.status == TaskStatusEnum.IN_PROGRESS:
                task.status = TaskStatusEnum.DONE
                await db.commit()
                return {"new_status": TaskStatusEnum.DONE}

        else:

            task.status = TaskStatusEnum.EXPIRED
            await db.commit()
            return {"new_status": TaskStatusEnum.EXPIRED}


    async def change_status(self,db: AsyncSession,new_status: TaskStatusEnum,id: int):
        result = await db.execute(select(TaskOrm).where(
            TaskOrm.id == id
        ))
        task = result.scalars().one_or_none()
        if not task:
            return None
        if task.deadline > datetime.now(ZoneInfo("Europe/Moscow")):
            task.status = new_status
            await db.commit()
            return True
        else:
            task.status = TaskStatusEnum.EXPIRED
            await db.commit()
            return False

    async def check_deadline(self,db: AsyncSession,id: int):
        result = await db.execute(select(TaskOrm).where(
            TaskOrm.id == id
        ))
        task = result.scalars().one_or_none()
        if not task:
            return None
        if task.deadline < datetime.now(ZoneInfo("Europe/Moscow")):
            task.status = TaskStatusEnum.EXPIRED
            await db.commit()
            return False
        else:
            return True

task_crud = TaskBaseCrud(TaskOrm)