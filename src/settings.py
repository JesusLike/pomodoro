from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_driver: str = ''
    db_username: str = ''
    db_password: str = ''
    db_host: str = ''
    db_port: int | None = None
    db_name: str = ''

    cache_host: str = ''
    cache_port: int | None = None
    cache_password: str = ''
    cache_expiry_time: int | None = None

    token_lifetime: int = 7
    token_encoding_key: str
    token_encoding_algorithm: str
    
    google_client_id: str = ''
    google_client_secret: str = ''
    google_redirect_uri: str = ''
    google_token_url: str = 'https://oauth2.googleapis.com/token'
    google_user_info_url: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    
    @property
    def google_auth_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.google_client_id}&redirect_uri={self.google_redirect_uri}&scope=openid%20profile%20email&access_type=offline"

    model_config = SettingsConfigDict(env_file='local.env', env_file_encoding='utf-8')

@lru_cache
def get_settings():
    return Settings()
