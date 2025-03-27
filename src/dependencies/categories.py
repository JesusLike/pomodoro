from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from src.caching.categories import CategoriesCacheRepository
from src.caching.core import get_cache
from src.controllers.categories import CategoriesController
from src.database.categories import CategoriesDatabaseRepository
from src.database.core import get_session
from src.settings import Settings, get_settings


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
