from pydantic import BaseModel

class RegisterSchema(BaseModel):
    name: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"