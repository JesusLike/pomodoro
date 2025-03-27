from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from .base import DbBase, PydanticBase

class InputCategory(PydanticBase):
    '''
    User input Category model
    '''
    name: str
    description: str | None = None

class PatchCategory(PydanticBase):
    '''
    Category model for partial update
    '''
    name: str | None = None
    description: str | None = None

class Category(InputCategory):
    id: int

class DbCategory(DbBase):
    '''
    Category model for storage 
    '''
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
