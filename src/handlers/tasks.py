'''
Tasks feature endpoints
'''

from typing import Annotated
from fastapi import APIRouter, Response, Request, Depends
from src.models.tasks import InputTask, Task, PatchTask
from src.controllers.tasks import TasksController
from src.dependencies.tasks import get_tasks_controller

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
    created = tasks.create_task(task)
    response.headers["Location"] = request.url.path + f"/{created.id}"
    return created

@router.put("/{task_id}", response_model=Task)
def update_task(tasks: TasksControllerDep, response: Response, task_id: int, new_task: InputTask):
    '''
    Update task
    '''
    return tasks.update_task(task_id, new_task)

@router.patch("/{task_id}", response_model=Task)
def patch_task(tasks: TasksControllerDep, response: Response, task_id: int, task_props: PatchTask):
    '''
    Update task properties
    '''
    return tasks.patch_task(task_id, task_props)

@router.get("/{task_id}", response_model=Task)
def get_task(tasks: TasksControllerDep, response: Response, task_id: int):
    '''
    Retrieve task
    '''
    return tasks.get_task(task_id)

@router.delete("/{task_id}")
def delete_task(tasks: TasksControllerDep, response: Response, task_id: int):
    ''' 
    Delete task
    '''
    return tasks.delete_task(task_id)
