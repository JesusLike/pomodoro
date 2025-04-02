from .base import AuthenticationError

class UserAlreadyExistsError(AuthenticationError):
    _message = "Something went wrong, try again later"

class UserInvalidCredentialsError(AuthenticationError):
    _message = "Username or password is invalid"

class UserNotFoundError(UserInvalidCredentialsError):
    pass

class UserIncorrectPasswordError(UserInvalidCredentialsError):
    pass

class UserInvalidTokenError(AuthenticationError):
    _message = "Access token is invalid or has expired"

class UserTokenExpiredError(UserInvalidTokenError):
    pass

class UserTokenNotFoundError(UserInvalidTokenError):
    pass
