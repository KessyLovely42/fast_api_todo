from fastapi import FastAPI, HTTPException
from schemas.models import *

api = FastAPI()

#Simulated database of the todo app
all_todos = [
    Todo(id = 1, name = "shop", description = "go buy some food", priority=Priority.HIGH),
    Todo(id = 2, name = "gym", description = "go buy some food", priority=Priority.MEDIUM),
    Todo(id = 3, name = "read", description = "go buy some food", priority=Priority.LOW),
    Todo(id = 4, name = "read", description = "go buy some food", priority=Priority.MEDIUM),
    Todo(id = 6, name = "hang out", description = "go buy some food", priority=Priority.LOW),
]

@api.get("/", response_model=List[Todo])
def get_todos(items: int = None):
    if items:
        return all_todos[:items]
    else:
        return all_todos


@api.get("/todo/{id}", response_model= Todo)
def get_todo(id: int):
    for todo in all_todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail="item not found")

# create to do 
@api.post("/add/", response_model=Todo)
def create_todo(todo: Todo):
    new_todo_id = len(all_todos)+1
    new_todo = Todo(
        id = new_todo_id,
        name = todo.name,
        description = todo.description,
        priority= todo.priority

    )

    all_todos.append(new_todo)

    return todo

        
# edit to do
@api.put("/update/{id}")
def edit_todo(id: int, todo: TodoUpdate):
    for index, to_do in enumerate(all_todos):
        if id == index:
            to_do.name = todo.name,
            to_do.description = todo.description    
        
            return {"message": f"Successfully updated todo with id: {id} ",
                    "data": to_do}
    return "Could not update"

# delete to do

@api.delete("/drop/{id}")
def delete_todo(id: int):
    for index, todo_item in enumerate(all_todos):
        if id == index:
            all_todos.pop(index)

            return{"message": f"Successfully deleted todo item number {id}"}
