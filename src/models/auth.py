from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import PydanticBase, DbBase

class AccessToken(PydanticBase):
    token: str

class DbAccessToken(DbBase):
    __tablename__: str = "Tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hashed_token: Mapped[str] = mapped_column(nullable=False)
    salt: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
