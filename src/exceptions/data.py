from .base import InvalidOperationError, ResourceNotFoundError

class TaskUnexistingCategoryError(InvalidOperationError):
    _message = "Category doesn't exist"

class CategoryTaskBoundError(InvalidOperationError):
    _message = "Cannot delete Category if there are Tasks in it"
    
class TaskNotFoundError(ResourceNotFoundError):
    _message = "Task not found"
    
class CategoryNotFoundError(ResourceNotFoundError):
    _message = "Category not found"