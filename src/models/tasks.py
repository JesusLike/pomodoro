from typing import Optional
from pydantic import model_validator
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import DbBase, PydanticBase

class InputTask(PydanticBase):
    '''
    User input Task model
    '''
    name: str | None = None
    description: str | None = None
    pomodoro_count: int
    category_id: int

    @model_validator(mode="before")
    @classmethod
    def must_be_name_or_description(cls, data: any):
        if isinstance(data, dict):
            if "name" not in data and "description" not in data:
                raise ValueError("Task must contain either name or description")
        return data

class PatchTask(PydanticBase):
    '''
    Task model for partial update
    '''
    name: str | None = None
    description: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

class Task(InputTask):
    id: int

class DbTask(DbBase):
    '''
    Task model for storage
    '''
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("Categories.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
