'''
Packaging API handler files
'''

from .ping import router as ping_router
from .tasks import router as tasks_router
from .categories import router as categories_router
from .users import router as users_router

routers = [ping_router, tasks_router, categories_router, users_router]
