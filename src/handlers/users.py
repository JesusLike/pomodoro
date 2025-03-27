from typing import Annotated
from fastapi import APIRouter, Depends

from src.models.users import UserLoginCredentials
from src.controllers.users import UsersController
from src.dependencies.users import get_users_controller

router = APIRouter(prefix="/users", tags=["users"])

UsersControllerDep = Annotated[UsersController, Depends(get_users_controller)]

@router.post("/create")
def create_user(users_controller: UsersControllerDep, credentials: UserLoginCredentials) -> UserLoginCredentials:
    return users_controller.create_user(credentials)
