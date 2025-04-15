from typing import Annotated

from fastapi import Depends, Security, security
from sqlalchemy.orm import Session

from src.client.google import GoogleClient
from src.controllers.auth import AuthController
from src.database.core import get_session
from src.database.users import UsersRepository
from src.database.tokens import TokensRepository
from src.dependencies.users import get_users_repository
from src.dependencies.security import decode_jwt_token
from src.settings import Settings, get_settings

def get_google_client(settings: Annotated[Settings, Depends(get_settings)]):
    return GoogleClient(settings=settings)

def get_tokens_repository(session_dep: Annotated[Session, Depends(get_session)]):
    return TokensRepository(session=session_dep)

def get_auth_controller(
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
        tokens_repository: Annotated[TokensRepository, Depends(get_tokens_repository)],
        google_client: Annotated[GoogleClient, Depends(get_google_client)],
        settings: Annotated[Settings, Depends(get_settings)]):
    return AuthController(
        users_repository=users_repository, 
        tokens_repository=tokens_repository, 
        google_client=google_client,
        settings=settings
    )

auth_schema = security.HTTPBearer()

def get_authorized_user(auth_controller: Annotated[AuthController, Depends(get_auth_controller)],
                        settings: Annotated[Settings, Depends(get_settings)],
                        credentials: security.http.HTTPAuthorizationCredentials = Security(auth_schema)) -> int | None:
    token = credentials.credentials
    token_content = decode_jwt_token(token, settings)
    user_id = token_content["sub"]
    if auth_controller.validate_token(user_id, token):
        return user_id
    return None

AuthorizedUserId = Annotated[int, Depends(get_authorized_user)]
