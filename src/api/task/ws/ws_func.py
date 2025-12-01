from fastapi import Depends,WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth_config import oauth2_scheme
from src.api.auth.auth_func import get_user_from_token
from src.api.task.task_crud import task_crud
from src.api.task.task_exceptions import TaskNotFoundException, DeadlinePassed
from src.api.users.users_exceptions import UserNotFoundException
from src.database import get_async_db


async def ws_task_func(websocket: WebSocket, token: str, db: AsyncSession):
    user_orm = await get_user_from_token(token, db)
    if not user_orm:
        await websocket.close(code=1008)
        return

    while True:
        try:
            data = await websocket.receive_text()
            if "break" in data:
                await websocket.close(code=1008)
                break
            res = await task_crud.check_deadline(db, int(data))
            if res is None:
                await websocket.send_text("Task not found")
            elif not res:
                await websocket.send_text("Deadline passed")
            else:
                await websocket.send_text("True")
        except Exception as e:
            await websocket.close(code=1011)
            break