import bcrypt

def hash_password(password: str) -> tuple[bytes, bytes]:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return (hashed_password, salt)