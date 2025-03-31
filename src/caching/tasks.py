from dataclasses import dataclass
from redis import Redis

from src.models.tasks import Task

@dataclass
class TasksCacheRepository:
    cache: Redis
    expiry_time: int

    def __expire(self, name: str) -> None:
        self.cache.expire(name, self.expiry_time)

    def get_tasks_by_user_id(self, user_id: int) -> list[Task] | None:
        if not self.cache.exists(f"tasks_{user_id}"):
            return None
        hash_list: list[str] = self.cache.lrange(f"tasks_{user_id}", 0, -1)
        tasks: list[Task] = []
        for hash_name in hash_list:
            tasks.append(Task.model_validate(self.cache.hgetall(hash_name)))
        return tasks

    def set_tasks_with_user_id(self, tasks: list[Task], user_id: int) -> None:
        for task in tasks:
            hash_name = f"task:{task.id}"
            self.cache.hset(hash_name, mapping=task.model_dump(exclude_none=True))
            self.__expire(hash_name)
            self.cache.lpush(f"tasks_{user_id}", hash_name)
        self.__expire(f"tasks_{user_id}")

    def get_task_with_user_id(self, id: int, user_id: int) -> Task | None:
        # implement redis indexing
        hash_name = f"task:{id}"
        hash_list = self.cache.lrange(f"tasks_{user_id}", 0, -1)
        if not hash_name in hash_list:
            return None
        return Task.model_validate(self.cache.hgetall(hash_name))

    def invalidate_with_user_id(self, user_id: int) -> None:
        self.cache.delete(f"tasks_{user_id}")
