from datetime import datetime, timezone, timedelta
import bcrypt
from jose import jwt, ExpiredSignatureError, JWTError

from src.exceptions.auth import UserTokenExpiredError, UserInvalidTokenError
from src.settings import Settings

def hash_secret(secret: str, salt: str | None = None) -> tuple[str, str]:
    if not salt:
        salt_bytes = bcrypt.gensalt()
        salt = salt_bytes.decode()
    else:
        salt_bytes = salt.encode()
    hashed_secret: bytes = bcrypt.hashpw(secret.encode(), salt_bytes)
    return (hashed_secret.decode(), salt)

def generate_jwt_token(user_id: int, settings: Settings) -> str:
    issued_at = datetime.now(timezone.utc)
    expiration_time = issued_at + timedelta(days=settings.token_lifetime)
    
    claims = {
        "sub": str(user_id),
        # TODO: JWT Claims
        # "iss": settings.get_api_identifier(),
        # "aud": [settings.get_api_identifier()],
        "exp": expiration_time,
        "iat": issued_at
    }
    return jwt.encode(claims, settings.token_encoding_key, algorithm=settings.token_encoding_algorithm)

def decode_jwt_token(token: str, settings: Settings) -> dict[str, str]:
    try:
        return jwt.decode(token, settings.token_encoding_key, algorithms=[settings.token_encoding_algorithm])
    except ExpiredSignatureError as e:
        raise UserTokenExpiredError() from e
    except JWTError as e:
        raise UserInvalidTokenError() from e