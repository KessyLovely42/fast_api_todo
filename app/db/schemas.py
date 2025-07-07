from typing import List, Optional
from datetime import datetime
from utils.utils import Priority

from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    """Base Class for the Todo Items"""
    #item name
    title: str = Field(..., min_length=3, max_length=512, description = "name of the todo Item")

    #item description
    description: Optional[str] = Field(None, description = "description of the to do item")

    #date and item was created
    created : Optional[datetime] = Field(None, description= "date and time todo was created")

    #if item is completed
    completed : Optional[bool] = Field(default=False, description="to indicate if task has been completed")

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
    id: Optional[str] = Field(None, description="unique identifier for the item")