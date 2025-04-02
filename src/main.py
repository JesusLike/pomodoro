'''
Application server entry point
'''

from fastapi import FastAPI
#from prometheus_fastapi_instrumentator import Instrumentator
from src.handlers import routers
from src.setup import setup_app

app = FastAPI()

for router in routers:
    app.include_router(router=router)

setup_app(app)

#
# Instrumentator().instrument(app).expose(app)
