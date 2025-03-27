'''
Tasks feature endpoints
'''

from typing import Annotated
from fastapi import APIRouter, Response, Request, Depends
from src.models.tasks import InputTask, Task, PatchTask
from src.controllers.tasks import TasksController
from src.dependencies.tasks import get_tasks_controller
from src.exceptions import DbException, ExternalException

router = APIRouter(prefix="/tasks", tags=["tasks"])

TasksControllerDep = Annotated[TasksController, Depends(get_tasks_controller)]

@router.get("", response_model=list[Task])
def get_tasks(tasks: TasksControllerDep):
    '''
    Retrieve all tasks
    '''
    return tasks.get_tasks()

@router.post("", status_code=201, response_model=Task)
def create_task(tasks: TasksControllerDep, response: Response, request: Request, task: InputTask):
    '''
    Create new task
    '''
    try:
        created = tasks.create_task(task)
    except DbException as e:
        raise ExternalException(e.args[0]) from e
    response.headers["Location"] = request.url.path + f"/{created.id}"
    return created

@router.put("/{task_id}", response_model=Task | None)
def update_task(tasks: TasksControllerDep, response: Response, task_id: int, new_task: InputTask):
    '''
    Update task
    '''
    if not (updated := tasks.update_task(task_id, new_task)):
        response.status_code = 404
    return updated

@router.patch("/{task_id}", response_model=Task | None)
def patch_task(tasks: TasksControllerDep, response: Response, task_id: int, task_props: PatchTask):
    '''
    Update task properties
    '''
    if not (updated := tasks.patch_task(task_id, task_props)):
        response.status_code = 404
    return updated

@router.get("/{task_id}", response_model=Task | None)
def get_task(tasks: TasksControllerDep, response: Response, task_id: int):
    '''
    Retrieve task
    '''
    if not (task := tasks.get_task(task_id)):
        response.status_code = 404
    return task

@router.delete("/{task_id}")
def delete_task(tasks: TasksControllerDep, response: Response, task_id: int):
    ''' 
    Delete task
    '''
    if not (deleted := tasks.delete_task(task_id)):
        response.status_code = 404
    return deleted
