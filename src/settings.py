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

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

@lru_cache
def get_settings():
    return Settings()
