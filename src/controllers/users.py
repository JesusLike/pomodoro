
from dataclasses import dataclass

import bcrypt

from src.database.users import UsersRepository
from src.exceptions import UserNameAlreadyExists
from src.models.users import UserLoginCredentials

@dataclass
class UsersController():
    users_repository: UsersRepository

    def create_user(self, credentials: UserLoginCredentials) -> UserLoginCredentials | None:
        username = credentials.username

        if self.users_repository.get_user(username):
            raise UserNameAlreadyExists()

        hashed_password, salt = self.__hash_passowrd(credentials.password)

        if not self.users_repository.create_user({
            "username": username,
            "hashed_password": hashed_password,
            "salt": salt
        }):
            return None

        return credentials

    @staticmethod
    def __hash_passowrd(password: str) -> tuple[bytes, bytes]:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return (hashed_password, salt)
