from fastapi import FastAPI

api = FastAPI()

#Simulated database of the todo app
all_todos = [
    {"id": 1, "name": "shop", "description": "go buy some food"},
    {"id": 2, "name": "gym", "description": "spend 20 mins at the gym"},
    {"id": 3, "name": "read", "description": "read 10 pages"},
    {"id": 4, "name": "jump", "description": "go jump from rooftop"},
    {"id": 5, "name": "hang out", "description": "go drink some beer"},
]

@api.get("/")
def index():
    return {"hello Godswill"}

@api.get("/todo/{id}")
def get_todo(id: int):
    for todo in all_todos:
        if todo["id"] == id:
            return todo
    
@api.get("/todos/")
def get_todos(items: int = None):
    if items:
        return all_todos[:items]
    else:
        return all_todos

# create to do 
@api.post("/add/")
def create_todo(todo: dict):
    if todo:
        todo["id"] = len(all_todos)+1

        todo["name"] = todo["name"]
        todo["description"] = todo["description"]

        all_todos.append(todo)

        return todo
    return ("Could not add todo")
        
# edit to do
@api.put("/update/{id}")
def edit_todo(id: int, todo: dict):
    for index, to_do in enumerate(all_todos):
        if id == index:
            to_do["name"] = todo["name"],
            to_do["description"] = todo["description"]     
        
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
