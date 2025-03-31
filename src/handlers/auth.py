from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from src.controllers.auth import AuthController
from src.dependencies.auth import get_auth_controller
from src.exceptions.exceptions import UserIncorrectPassword, UserNotFound
from src.models.users import UserLoginCredentials
from src.models.auth import AccessToken

router = APIRouter(prefix="/auth", tags=["auth"])

AuthControllerDep = Annotated[AuthController, Depends(get_auth_controller)]

@router.post("/login")
def login_with_credentials(auth_controller: AuthControllerDep, credentials: UserLoginCredentials) -> AccessToken:
    try:
        token = auth_controller.login_with_credentials(credentials)
    except (UserNotFound, UserIncorrectPassword) as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    return token
