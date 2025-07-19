from typing import List, Optional
from datetime import datetime
from utils import Priority

from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    #id of the item 
    id: int = Field(description="unique identifier for the item")

    #item name
    title: str = Field(description = "title of the todo Item")

    #item description
    description: Optional[str] = Field(description = "description of the to do item")

    #date and item was created
    created : datetime = Field(description= "date and time todo was created")

    #if item is completed
    completed : bool = Field(description="to indicate if task has been completed")

    #item priority
    priority : Priority = Field(description = "priority of the to do item" )

class TodoResponse(BaseModel):

    #item name
    title: str = Field(description = "title of the todo Item")

    #item description
    description: Optional[str] = Field(description = "description of the to do item")

    #date and item was created
    created : datetime = Field(description= "date and time todo was created")

    #if item is completed
    completed : bool = Field(description="to indicate if task has been completed")

    #item priority
    priority : Priority = Field(description = "priority of the to do item" )

class TodoCreate(BaseModel):
    #item name
    title: str = Field(..., min_length=3, description = "name of the todo Item")

    #item description
    description: Optional[str] = Field(None, min_length=3, max_length=512, description = "description of the to do item")

    #if item is completed
    completed : Optional[bool] = Field(default=False, description="to indicate if task has been completed")

    #item priority
    priority : Priority = Field(default = Priority.LOW, description = "priority of the to do item" )

class TodoUpdate(BaseModel):

    #item name
    title: Optional[str] = Field(None, min_length=3, max_length=512, description = "name of the todo Item")

    #item description 
    description: Optional[str] = Field(None, description = "description of the to do item" )

    #if item is completed
    completed : Optional[bool] = Field(description="to indicate if task has been completed")

    #item priority
    priority: Optional[Priority] = Field(None,  description = "priority of the to do item" )