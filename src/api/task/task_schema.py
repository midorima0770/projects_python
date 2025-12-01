from datetime import datetime

from pydantic import BaseModel
from pydantic.v1 import Field


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    deadline:datetime
    project_id: int
    assignee_id: int = Field(default=None)