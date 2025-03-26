from dataclasses import dataclass
from redis import Redis

from src.models.tasks import Task

@dataclass
class TasksCacheRepository:
    cache: Redis
    expiry_time: int

    def __expire(self, name: str) -> None:
        self.cache.expire(name, self.expiry_time)

    def get_tasks(self) -> list[Task] | None:
        if not self.cache.exists("tasks"):
            return None
        hash_list: list[str] = self.cache.lrange("tasks", 0, -1)
        tasks: list[Task] = []
        for hash_name in hash_list:
            tasks.append(Task.model_validate(self.cache.hgetall(hash_name)))
        return tasks

    def set_tasks(self, tasks: list[Task]) -> None:
        for task in tasks:
            hash_name = f"task:{task.id}"
            self.cache.hset(hash_name, mapping=task.model_dump(exclude_none=True))
            self.__expire(hash_name)
            self.cache.lpush("tasks", hash_name)
        self.__expire("tasks")

    def get_task(self, id: int) -> Task | None:
        # implement redis indexing
        hash_name = f"task:{id}"
        hash_list = self.cache.lrange("tasks", 0, -1)
        if not hash_name in hash_list:
            return None
        return Task.model_validate(self.cache.hgetall(hash_name))

    def invalidate(self) -> None:
        self.cache.delete("tasks")
