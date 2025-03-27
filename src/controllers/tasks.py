from dataclasses import dataclass

from src.models.tasks import Task, PatchTask, InputTask
from src.caching.tasks import TasksCacheRepository
from src.database.tasks import TasksDatabaseRepository

@dataclass
class TasksController:
    cache_repository: TasksCacheRepository
    db_repository: TasksDatabaseRepository

    def get_tasks(self):
        if cached := self.cache_repository.get_tasks():
            return cached
        tasks = [Task.model_validate(db_task) for db_task in self.db_repository.get_tasks()]
        self.cache_repository.set_tasks(tasks)
        return tasks

    def get_task(self, id: int) -> Task | None:
        if cached := self.cache_repository.get_task(id):
            return cached
        if not (db_task := self.db_repository.get_task(id)):
            return None
        return Task.model_validate(db_task)

    def create_task(self, task: InputTask) -> Task:
        db_task = self.db_repository.create_task(task.model_dump())
        self.cache_repository.invalidate()
        return Task.model_validate(db_task)

    def update_task(self, id: int, task: InputTask) -> Task | None:
        if not (db_task := self.db_repository.update_task(id, task.model_dump())):
            return None
        self.cache_repository.invalidate()
        return Task.model_validate(db_task)

    def patch_task(self, id: int, props: PatchTask) -> Task | None:
        if not (db_task := self.db_repository.update_task(id, props.model_dump(exclude_none=True))):
            return None
        self.cache_repository.invalidate()
        return Task.model_validate(db_task)

    def delete_task(self, id: int) -> Task | None:
        if not (db_task := self.db_repository.delete_task(id)):
            return None
        self.cache_repository.invalidate()
        return Task.model_validate(db_task)
