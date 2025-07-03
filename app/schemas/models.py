from typing import List, Optional
from utils.utils import Priority

from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    """Base Class for the Todo Items"""
    #item name
    name: str = Field(..., min_length=3, max_length=512, description = "name of the todo Item")

    #item description
    description: str = Field(..., description = "description of the to do item")

    #item priority
    priority : Priority = Field(default = Priority.LOW, description = "priority of the to do item" )

class TodoCreate(TodoBase):
    """Class Model for the creating todo Items"""
    pass 

class TodoUpdate(TodoBase):
    #item name
    name: Optional[str] = Field(None, min_length=3, max_length=512, description = "name of the todo Item")

    #item description 
    description: Optional[str] = Field(None, description = "description of the to do item" )

    #item priority
    priority: Optional[Priority] = Field(None,  description = "priority of the to do item" )

class Todo(TodoBase):
    #id of the item 
    id: int = Field(..., description="unique identifier for the item")