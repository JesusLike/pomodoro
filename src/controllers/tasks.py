from dataclasses import dataclass

from src.models.tasks import Task, PatchTask, InputTask
from src.caching.tasks import TasksCacheRepository
from src.database.tasks import TasksDatabaseRepository

@dataclass
class TasksController:
    cache_repository: TasksCacheRepository
    db_repository: TasksDatabaseRepository
    user_id: int

    def get_tasks(self):
        if cached := self.cache_repository.get_tasks_by_user_id(self.user_id):
            return cached
        tasks = [Task.model_validate(db_task) for db_task in self.db_repository.get_tasks_by_user_id(self.user_id)]
        self.cache_repository.set_tasks_with_user_id(tasks, self.user_id)
        return tasks

    def get_task(self, id: int) -> Task | None:
        if cached := self.cache_repository.get_task_with_user_id(id, self.user_id):
            return cached
        if not (db_task := self.db_repository.get_task_with_user_id(id, self.user_id)):
            return None
        return Task.model_validate(db_task)

    def create_task(self, task: InputTask) -> Task:
        props = task.model_dump()
        props.update({ "user_id": self.user_id })
        db_task = self.db_repository.create_task(props)
        self.cache_repository.invalidate_with_user_id(self.user_id)
        return Task.model_validate(db_task)

    def update_task(self, id: int, task: InputTask) -> Task | None:
        if not (db_task := self.db_repository.update_task_with_user_id(id, self.user_id, task.model_dump())):
            return None
        self.cache_repository.invalidate_with_user_id(self.user_id)
        return Task.model_validate(db_task)

    def patch_task(self, id: int, props: PatchTask) -> Task | None:
        if not (db_task := self.db_repository.update_task_with_user_id(id, self.user_id, props.model_dump(exclude_none=True))):
            return None
        self.cache_repository.invalidate_with_user_id(self.user_id)
        return Task.model_validate(db_task)

    def delete_task(self, id: int) -> Task | None:
        if not (db_task := self.db_repository.delete_task_with_user_id(id, self.user_id)):
            return None
        self.cache_repository.invalidate_with_user_id(self.user_id)
        return Task.model_validate(db_task)
