from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis

from src.settings import Settings, get_settings

from src.database.core import get_session
from src.database.tasks import TasksDatabaseRepository
from src.database.categories import CategoriesDatabaseRepository
from src.database.users import UsersRepository

from src.caching.core import get_cache
from src.caching.tasks import TasksCacheRepository
from src.caching.categories import CategoriesCacheRepository

from src.controllers.tasks import TasksController
from src.controllers.categories import CategoriesController
from src.controllers.users import UsersController

# --- Tasks dependencies

def get_tasks_database_repository(session_dep: Annotated[Session, Depends(get_session)]):
    return TasksDatabaseRepository(session=session_dep)

def get_tasks_cache_repository(
        cache_dep: Annotated[Redis, Depends(get_cache)],
        settings: Annotated[Settings, Depends(get_settings)]
    ):
    return TasksCacheRepository(cache=cache_dep, expiry_time=settings.cache_expiry_time)

def get_tasks_controller(
        cache_repository_dep: Annotated[TasksCacheRepository, Depends(get_tasks_cache_repository)],
        db_repository_dep: Annotated[TasksDatabaseRepository, Depends(get_tasks_database_repository)]
    ):
    return TasksController(cache_repository=cache_repository_dep, db_repository=db_repository_dep)

# --- Categories dependencies

def get_categories_database_repository(session_dep: Annotated[Session, Depends(get_session)]):
    return CategoriesDatabaseRepository(session=session_dep)

def get_categories_cache_repository(
        cache_dep: Annotated[Redis, Depends(get_cache)],
        settings: Annotated[Settings, Depends(get_settings)]
    ):
    return CategoriesCacheRepository(cache=cache_dep, expiry_time=settings.cache_expiry_time)

def get_categories_controller(
        cache_repository_dep: Annotated[CategoriesCacheRepository, Depends(get_categories_cache_repository)],
        db_repository_dep: Annotated[CategoriesDatabaseRepository, Depends(get_categories_database_repository)]
    ):
    return CategoriesController(cache_repository=cache_repository_dep, db_repository=db_repository_dep)

# --- Users dependencies

def get_users_repository(session_dep: Annotated[Session, Depends(get_session)]):
    return UsersRepository(session=session_dep)

def get_users_controller(db_repository_dep: Annotated[UsersRepository, Depends(get_users_repository)]):
    return UsersController(users_repository=db_repository_dep)
