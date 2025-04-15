from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.controllers.auth import AuthController
from src.dependencies.auth import get_auth_controller
from src.models.users import UserLoginCredentials
from src.models.auth import AccessToken

router = APIRouter(prefix="/auth", tags=["auth"])

AuthControllerDep = Annotated[AuthController, Depends(get_auth_controller)]

@router.post("/login")
def login_with_credentials(auth_controller: AuthControllerDep, credentials: UserLoginCredentials) -> AccessToken:
    return auth_controller.login_with_credentials(credentials)

@router.get("/google", response_class=RedirectResponse)
def login_with_google(auth_controller: AuthControllerDep):
    return RedirectResponse(auth_controller.get_google_auth_redirect_url())

@router.get("/google/redirect")
def auth_google(auth_controller: AuthControllerDep, code: str):
    return auth_controller.login_with_google(code)
