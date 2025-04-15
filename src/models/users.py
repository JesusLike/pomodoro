from sqlalchemy.orm import Mapped, mapped_column

from .base import PydanticBase, DbBase

class UserLoginCredentials(PydanticBase):
    username: str
    password: str

class DbUser(DbBase):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True) # TODO: change into email
    hashed_password: Mapped[str] = mapped_column(nullable=True, unique=True)
    salt: Mapped[str] = mapped_column(nullable=True, unique=True)
