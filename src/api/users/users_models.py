from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from src.models import Base

class RoleEnum(str, enum.Enum):
    user="user"
    admin="admin"
    owner="owner"

class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String,nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum),nullable=False)

    projects = relationship("ProjectOrm", back_populates="owner", cascade="all, delete")
