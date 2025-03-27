
from dataclasses import dataclass

from src.database.users import UsersRepository
from src.exceptions import UserAlreadyExists
from src.models.users import UserLoginCredentials

from src.dependencies.security import hash_password

@dataclass
class UsersController():
    users_repository: UsersRepository

    def create_user(self, credentials: UserLoginCredentials) -> UserLoginCredentials | None:
        username = credentials.username

        if self.users_repository.get_user(username):
            raise UserAlreadyExists()

        hashed_password, salt = hash_password(credentials.password)

        if not self.users_repository.create_user({
            "username": username,
            "hashed_password": hashed_password,
            "salt": salt
        }):
            return None

        return credentials
