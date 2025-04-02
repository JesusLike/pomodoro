from fastapi import FastAPI, HTTPException, Request
from src.exceptions.base import ClientErrorBase

def __setup_exceptions(app: FastAPI):
    @app.exception_handler(ClientErrorBase)
    def incorrect_credentials_handler(request: Request, exception: ClientErrorBase):
        raise HTTPException(
            status_code=exception.status_code,
            detail=exception.message
        )
        
def setup_app(app: FastAPI):
    __setup_exceptions(app)