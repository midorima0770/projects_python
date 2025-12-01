from pydantic import BaseModel
from pydantic.v1 import Field


class CreateProjectSchema(BaseModel):
    title: str
    description: str
    owner_id: int

class ChangeTitleSchema(BaseModel):
    id: int
    new_title: str

class ChangeDescriptionSchema(BaseModel):
    id: int
    new_description: str