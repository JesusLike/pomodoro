from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.tasks import DbTask
from src.exceptions import DbException

@dataclass
class TasksDatabaseRepository():
    session: Session

    def get_tasks_by_user_id(self, user_id: int) -> list[DbTask]:
        query = select(DbTask).where(DbTask.user_id == user_id)
        return self.session.execute(query).scalars().all()

    def create_task(self, props: dict[str, any]) -> DbTask:
        db_task = DbTask(**props)
        self.session.add(db_task)
        try:
            self.session.commit()
        except IntegrityError as e:
            raise DbException("Cannot create Task with unexisting Category") from e
        return db_task

    def get_task_with_user_id(self, id: int, user_id: int) -> DbTask | None:
        print(user_id)
        query = select(DbTask).where(DbTask.id == id).where(DbTask.user_id == user_id)
        return self.session.execute(query).scalar_one_or_none()

    def update_task_with_user_id(self, id: int, user_id: int, props: dict[str, any]) -> DbTask | None:
        query = select(DbTask).where(DbTask.id == id).where(DbTask.user_id == user_id)
        if not (db_task := self.session.execute(query).scalar_one_or_none()):
            return None
        for name, value in props.items():
            setattr(db_task, name, value)
        self.session.commit()
        return db_task

    def delete_task_with_user_id(self, id: int, user_id: int) -> DbTask | None:
        query = select(DbTask).where(DbTask.id == id).where(DbTask.user_id == user_id)
        if not (db_task := self.session.execute(query).scalar_one_or_none()):
            return None
        self.session.delete(db_task)
        self.session.commit()
        return db_task
