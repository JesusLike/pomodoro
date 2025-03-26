'''
Healthcheck endpoints
'''

from typing import Annotated
from fastapi import APIRouter, Depends
from src.settings import Settings, get_settings

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("")
def ping_app():
    '''
    Check that application server is up
    '''
    return { "message": "Webserver is online" }

@router.get("/db")
def ping_db():
    '''
    Check that database is up
    '''
    return { "message": "Ping Database endpoint stub" }

@router.get("/db_name")
def check_token(settings: Annotated[Settings, Depends(get_settings)]):
    '''
    Get database name
    '''
    return { "token_id": settings.sqlite_db_name }
