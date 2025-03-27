from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from src.settings import get_settings

settings = get_settings()

def get_url():
    return URL.create(
        settings.db_driver,
        username=settings.db_username,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name
    )

url = get_url()
engine = create_engine(url)
session_maker = sessionmaker(engine)

async def get_session():
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
