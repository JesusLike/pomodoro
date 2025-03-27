import bcrypt

def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if not salt:
        salt_bytes = bcrypt.gensalt()
        salt = salt_bytes.decode()
    else:
        salt_bytes = salt.encode()
    hashed_password: bytes = bcrypt.hashpw(password.encode(), salt_bytes)
    return (hashed_password.decode(), salt)