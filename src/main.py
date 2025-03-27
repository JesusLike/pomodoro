'''
Application server entry point
'''

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
#from prometheus_fastapi_instrumentator import Instrumentator
from src.handlers import routers
from src.exceptions import ExternalException

app = FastAPI()

for router in routers:
    app.include_router(router=router)

@app.exception_handler(ExternalException)
def external_exception_handler(request: Request, exception: ExternalException):
    return JSONResponse(
        status_code=500,
        content={ "message": exception.args[0]}
    )

#
# Instrumentator().instrument(app).expose(app)
