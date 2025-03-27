class DbException(Exception):
    pass

class ExternalException(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

class UserNotFound(Exception):
    pass

class UserIncorrectPassword(Exception):
    pass