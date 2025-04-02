from dataclasses import dataclass

from src.database.users import UsersRepository
from src.database.tokens import TokensRepository
from src.dependencies.security import hash_secret, generate_jwt_token
from src.exceptions.auth import UserNotFoundError, UserIncorrectPasswordError, UserTokenNotFoundError
from src.models.users import UserLoginCredentials
from src.models.auth import AccessToken
from src.settings import Settings

@dataclass
class AuthController:
    users_repository: UsersRepository
    tokens_repository: TokensRepository
    settings: Settings

    def login_with_credentials(self, credentials: UserLoginCredentials) -> AccessToken:
        if not (db_user := self.users_repository.get_user(credentials.username)):
            raise UserNotFoundError()
        hashed_password = hash_secret(credentials.password, db_user.salt)[0]
        if hashed_password != db_user.hashed_password:
            raise UserIncorrectPasswordError()
        return self.create_jwt_token(db_user.id)

    def create_jwt_token(self, user_id: int) -> AccessToken:
        token = generate_jwt_token(user_id=user_id, settings=self.settings)
        hashed_token, salt = hash_secret(token)
        self.tokens_repository.create_token({
            "user_id": user_id, 
            "hashed_token": hashed_token, 
            "salt": salt
        })
        return AccessToken.model_validate({ "token": token })

    def validate_token(self, user_id: int, token: str) -> bool:
        db_user_tokens = self.tokens_repository.get_tokens(user_id)
        for db_token in db_user_tokens:
            hash = hash_secret(token, db_token.salt)[0]
            if hash == db_token.hashed_token:
                return True
        raise UserTokenNotFoundError()
