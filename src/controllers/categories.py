from dataclasses import dataclass

from src.models.categories import Category, PatchCategory, InputCategory
from src.caching.categories import CategoriesCacheRepository
from src.database.categories import CategoriesDatabaseRepository

@dataclass
class CategoriesController:
    cache_repository: CategoriesCacheRepository
    db_repository: CategoriesDatabaseRepository

    def get_categories(self):
        if cached := self.cache_repository.get_categories():
            return cached
        categories = [Category.model_validate(db_category) for db_category in self.db_repository.get_categories()]
        self.cache_repository.set_categories(categories)
        return categories

    def get_category(self, id: int) -> Category | None:
        if cached := self.cache_repository.get_category(id):
            return cached
        if not (db_category := self.db_repository.get_category(id)):
            return None
        return Category.model_validate(db_category)

    def create_category(self, category: InputCategory) -> Category:
        db_category = self.db_repository.create_category(category.model_dump())
        self.cache_repository.invalidate()
        return Category.model_validate(db_category)

    def update_category(self, id: int, category: InputCategory) -> Category | None:
        if not (db_category := self.db_repository.update_category(id, category.model_dump())):
            return None
        self.cache_repository.invalidate()
        return Category.model_validate(db_category)

    def patch_category(self, id: int, props: PatchCategory) -> Category | None:
        if not (db_category := self.db_repository.update_category(id, props.model_dump(exclude_none=True))):
            return None
        self.cache_repository.invalidate()
        return Category.model_validate(db_category)

    def delete_category(self, id: int) -> Category | None:
        if not (db_category := self.db_repository.delete_category(id)):
            return None
        self.cache_repository.invalidate()
        return Category.model_validate(db_category)
