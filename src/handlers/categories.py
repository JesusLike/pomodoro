'''
Categories feature endpoints
'''

from typing import Annotated
from fastapi import APIRouter, Response, Request, Depends
from src.models.categories import InputCategory, Category, PatchCategory
from src.controllers.categories import CategoriesController
from src.dependencies.categories import get_categories_controller

router = APIRouter(prefix="/categories", tags=["categories"])

CategoriesControllerDep = Annotated[CategoriesController, Depends(get_categories_controller)]

@router.get("", response_model=list[Category])
def get_categories(categories: CategoriesControllerDep):
    '''
    Retrieve all categories
    '''
    return categories.get_categories()

@router.post("", status_code=201, response_model=Category)
def create_category(categories: CategoriesControllerDep, response: Response, request: Request, category: InputCategory):
    '''
    Create new category
    '''
    created = categories.create_category(category)
    response.headers["Location"] = request.url.path + f"/{created.id}"
    return created

@router.put("/{category_id}", response_model=Category)
def update_category(categories: CategoriesControllerDep, category_id: int, new_category: InputCategory):
    '''
    Update category
    '''
    return categories.update_category(category_id, new_category)

@router.patch("/{category_id}", response_model=Category)
def patch_category(categories: CategoriesControllerDep, category_id: int, category_props: PatchCategory):
    '''
    Update category properties
    '''
    return categories.patch_category(category_id, category_props)

@router.get("/{category_id}", response_model=Category)
def get_category(categories: CategoriesControllerDep, category_id: int):
    '''
    Retrieve category
    '''
    return categories.get_category(category_id)

@router.delete("/{category_id}")
def delete_category(categories: CategoriesControllerDep, category_id: int):
    ''' 
    Delete category
    '''
    return categories.delete_category(category_id)
