from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from src.caching.core import get_cache
from src.caching.tasks import TasksCacheRepository
from src.controllers.tasks import TasksController
from src.database.core import get_session
from src.database.tasks import TasksDatabaseRepository
from src.dependencies.auth import AuthorizedUserId
from src.settings import Settings, get_settings


def get_tasks_database_repository(session_dep: Annotated[Session, Depends(get_session)]):
    return TasksDatabaseRepository(session=session_dep)

def get_tasks_cache_repository(
        cache_dep: Annotated[Redis, Depends(get_cache)],
        settings: Annotated[Settings, Depends(get_settings)]
    ):
    return TasksCacheRepository(cache=cache_dep, expiry_time=settings.cache_expiry_time)

def get_tasks_controller(
        cache_repository_dep: Annotated[TasksCacheRepository, Depends(get_tasks_cache_repository)],
        db_repository_dep: Annotated[TasksDatabaseRepository, Depends(get_tasks_database_repository)],
        user_id: AuthorizedUserId
    ):
    return TasksController(cache_repository=cache_repository_dep, db_repository=db_repository_dep, user_id=user_id)
