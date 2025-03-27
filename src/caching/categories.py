from dataclasses import dataclass
from redis import Redis

from src.models.categories import Category

@dataclass
class CategoriesCacheRepository:
    cache: Redis
    expiry_time: int

    def __expire(self, name: str) -> None:
        self.cache.expire(name, self.expiry_time)

    def get_categories(self) -> list[Category] | None:
        if not self.cache.exists("categories"):
            return None
        hash_list: list[str] = self.cache.lrange("categories", 0, -1)
        categories: list[Category] = []
        for hash_name in hash_list:
            categories.append(Category.model_validate(self.cache.hgetall(hash_name)))
        return categories

    def set_categories(self, categories: list[Category]) -> None:
        for category in categories:
            hash_name = f"category:{category.id}"
            self.cache.hset(hash_name, mapping=category.model_dump(exclude_none=True))
            self.__expire(hash_name)
            self.cache.lpush("categories", hash_name)
        self.__expire("categories")

    def get_category(self, id: int) -> Category | None:
        # implement redis indexing
        hash_name = f"category:{id}"
        hash_list = self.cache.lrange("categories", 0, -1)
        if not hash_name in hash_list:
            return None
        return Category.model_validate(self.cache.hgetall(hash_name))

    def invalidate(self) -> None:
        self.cache.delete("categories")
