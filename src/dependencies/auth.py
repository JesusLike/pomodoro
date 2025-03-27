from typing import Annotated

from fastapi import Depends

from src.controllers.auth import AuthController
from src.database.users import UsersRepository
from src.dependencies.users import get_users_repository


def get_auth_controller(users_repository: Annotated[UsersRepository, Depends(get_users_repository)]):
    return AuthController(users_repository=users_repository)