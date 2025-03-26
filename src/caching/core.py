import redis

from src.settings import get_settings

settings = get_settings()

def get_cache() -> redis.Redis:
    return redis.Redis(host=settings.cache_host, port=settings.cache_port, password=settings.cache_password, db=0, decode_responses=True)
