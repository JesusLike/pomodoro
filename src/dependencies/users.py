from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.controllers.users import UsersController
from src.database.core import get_session
from src.database.users import UsersRepository

def get_users_repository(session_dep: Annotated[Session, Depends(get_session)]):
    return UsersRepository(session=session_dep)

def get_users_controller(db_repository_dep: Annotated[UsersRepository, Depends(get_users_repository)]):
    return UsersController(users_repository=db_repository_dep)
