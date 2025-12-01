from fastapi import APIRouter,status

from src.database import create_all_tables, engine, drop_all_tables
from src.api.users.users_models import UserOrm

db = APIRouter(tags=["db"])

@db.post("/create",status_code=status.HTTP_201_CREATED)
async def create_db():
    await drop_all_tables(engine)
    await create_all_tables(engine)
    return{"status":status.HTTP_201_CREATED}
