from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.users import DbUser

@dataclass
class UsersRepository():
    session: Session

    def get_user(self, username: str) -> DbUser | None:
        query = select(DbUser).where(DbUser.username == username)
        return self.session.execute(query).scalar_one_or_none()

    def create_user(self, props: dict[str, any]) -> DbUser:
        db_user = DbUser(**props)
        self.session.add(db_user)
        self.session.commit()
        return db_user

    def update_user(self, id: int, props: dict[str, any]) -> DbUser:
        if not (db_user := self.__select_by_id(id)):
            return None
        for name, value in props.items():
            setattr(db_user, name, value)
        self.session.commit()
        return db_user

# --- Query creation methods

    def __select_by_id(self, id: int) -> DbUser | None:
        query = select(DbUser).where(DbUser.id == id)
        return self.session.execute(query).scalar_one_or_none()
