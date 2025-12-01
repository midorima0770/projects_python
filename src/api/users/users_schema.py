from pydantic import BaseModel

# User
class UserSchema(BaseModel):
    name: str

# Schema для возвращения пользователей
class UsersReturnSchema(BaseModel):
    status: int
    users: list[UserSchema]