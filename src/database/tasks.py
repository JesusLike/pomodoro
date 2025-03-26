from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.tasks import DbTask
from src.exceptions import DbException

@dataclass
class TasksDatabaseRepository():
    session: Session
    
    def get_tasks(self) -> list[DbTask]:
        return self.__select_all()

    def create_task(self, task: dict[str, any]) -> DbTask:
        db_task = self.__create(task)
        try:
            self.session.commit()
        except IntegrityError:
            raise DbException("Cannot create Task with unexisting Category")
        return db_task

    def get_task(self, id: int) -> DbTask | None:
        if not (db_task := self.__select_by_id(id)):
            return None
        return db_task

    def update_task(self, id: int, props: dict[str, any]) -> DbTask | None:
        if not (db_task := self.__select_by_id(id)):
            return None
        for name, value in props.items():
            db_task.__setattr__(name, value)
        self.session.commit()
        return db_task

    def delete_task(self, id: int) -> DbTask | None:
        if not (db_task := self.__select_by_id(id)):
            return None    
        self.session.delete(db_task)
        self.session.commit()
        return db_task

# --- Query creation methods ---

    def __create(self, values: dict[str, any]) -> DbTask:
        db_task = DbTask(**values)
        self.session.add(db_task)
        return db_task

    def __select_all(self) -> list[DbTask]:
        query = select(DbTask)
        return self.session.execute(query).scalars().all()

    def __select_by_id(self, id: int) -> DbTask | None:
        query = select(DbTask).where(DbTask.id == id)
        return self.session.execute(query).scalar_one_or_none()

# Core-style delete:
#
# def delete_task(id: int) -> Task | None:
#     query = delete(DbTask).where(DbTask.id == id)
#     with get_session() as session:
#         result = session.execute(query)
#         session.commit()
#     return result.rowcount
    
# Core-style update:
#
# def update_task(id: int, props: PatchTask, exclude_none: bool = False) -> int:
#    query = update(DbTask).where(DbTask.id == id).values(props.model_dump(exclude_none=exclude_none))
#    with get_session() as session:
#        result = session.execute(query)
#        session.commit()
#    return result.rowcount