from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.db.base_crud import BaseCRUD
from src.api.project.project_models import ProjectOrm
from src.api.project.project_schema import CreateProjectSchema
from src.api.users.users_models import RoleEnum

from sqlalchemy import func

from zoneinfo import ZoneInfo

class ProjectBaseCrud(BaseCRUD):

    model=ProjectOrm

    async def get_all_projects(self,db: AsyncSession,user_id: int,user_role: RoleEnum):
        if user_role == RoleEnum.user:
            result = await db.execute(select(ProjectOrm)
            .options(selectinload(ProjectOrm.tasks))
            .where(
                ProjectOrm.owner_id==user_id
            ))
            projects = result.scalars().all()
            return projects
        else:
            result = await db.execute(select(ProjectOrm).options(selectinload(ProjectOrm.tasks)))
            projects = result.scalars().all()
            return projects

    async def get_project_by_id(self,db: AsyncSession,id: int):
        result = await db.execute(select(ProjectOrm)
        .options(selectinload(ProjectOrm.tasks))
        .where(
            ProjectOrm.id == id
        ))
        project = result.scalars().one_or_none()
        return project

    async def check_project_is_already(self,db: AsyncSession,title: str,owner_id: int):
        result = await db.execute(
            select(ProjectOrm).where(
                func.lower(ProjectOrm.title) == func.lower(title),
                ProjectOrm.owner_id == owner_id
            )
        )
        project = result.scalars().one_or_none()
        return project

    async def check_project_is_already_by_id(self,db: AsyncSession, id: int):
        result = await db.execute(select(ProjectOrm).where(
            ProjectOrm.id == id
        ))
        project = result.scalars().one_or_none()
        return project

    async def create_project(self,db: AsyncSession,new_project: CreateProjectSchema):
        project_orm = ProjectOrm(
            title=new_project.title,
            description=new_project.description,
            created_at=datetime.now(ZoneInfo("Europe/Moscow")),
            owner_id=new_project.owner_id
        )
        db.add(project_orm)
        await db.commit()

    async def delete_project(self,db: AsyncSession,id: int):
        result = await db.execute(select(ProjectOrm).where(
            ProjectOrm.id == id
        ))
        project = result.scalars().one_or_none()
        if not project:
            return False
        await db.delete(project)
        await db.commit()
        return True

    async def change_title(self,db: AsyncSession,id: int,new_title: str):
        result = await db.execute(select(ProjectOrm).where(
            ProjectOrm.id == id
        ))
        project = result.scalars().one_or_none()
        if not project:
            return False
        else:
            project.title = new_title
            await db.commit()
            await db.refresh(project)
            return project

    async def change_description(self,db: AsyncSession,id: int,new_description: str):
        result = await db.execute(select(ProjectOrm).where(
            ProjectOrm.id == id
        ))
        project = result.scalars().one_or_none()
        if not project:
            return False
        else:
            project.description = new_description
            await db.commit()
            await db.refresh(project)
            return project

project_crud = ProjectBaseCrud(ProjectOrm)