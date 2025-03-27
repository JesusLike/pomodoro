from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.categories import DbCategory
from src.exceptions import DbException

@dataclass
class CategoriesDatabaseRepository():
    session: Session

    def get_categories(self) -> list[DbCategory]:
        return self.__select_all()

    def create_category(self, category: dict[str, any]) -> DbCategory:
        db_category = self.__create(category)
        self.session.commit()
        return db_category

    def get_category(self, id: int) -> DbCategory | None:
        if not (db_category := self.__select_by_id(id)):
            return None
        return db_category

    def update_category(self, id: int, props: dict[str, any]) -> DbCategory | None:
        if not (db_category := self.__select_by_id(id)):
            return None
        for name, value in props.items():
            setattr(db_category, name, value)
        self.session.commit()
        return db_category

    def delete_category(self, id: int) -> DbCategory | None:
        if not (db_category := self.__select_by_id(id)):
            return None
        self.session.delete(db_category)
        try:
            self.session.commit()
        except IntegrityError as e:
            raise DbException("Cannot delete Category if it is referenced by any Task") from e
        return db_category

# --- Query creation methods ---

    def __create(self, values: dict[str, any]) -> DbCategory:
        db_category = DbCategory(**values)
        self.session.add(db_category)
        return db_category

    def __select_all(self) -> list[DbCategory]:
        query = select(DbCategory)
        return self.session.execute(query).scalars().all()

    def __select_by_id(self, id: int) -> DbCategory | None:
        query = select(DbCategory).where(DbCategory.id == id)
        return self.session.execute(query).scalar_one_or_none()
