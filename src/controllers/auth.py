from dataclasses import dataclass

from src.database.users import UsersRepository
from src.dependencies.security import hash_password
from src.exceptions.exceptions import UserNotFound, UserIncorrectPassword
from src.models.users import UserLoginCredentials


@dataclass
class AuthController:
    users_repository: UsersRepository
    
    def check_credentials(self, credentials: UserLoginCredentials) -> bool:
        if not (db_user := self.users_repository.get_user(credentials.username)):
            raise UserNotFound()
        hashed_password = hash_password(credentials.password, db_user.salt)[0]
        if hashed_password != db_user.hashed_password:
            raise UserIncorrectPassword()
        return True