from uuid import uuid4
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from db.schemas import *
from db.models import Base, todos
from db.db_con import engine, SessionDep
from datetime import datetime

from random import randint


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def get_todos():
    return "hello"

# @api.get("/todo/{id}", response_model= Todo)
# def get_todo(id: int):
#     for todo in all_todos:
#         if todo.id == id:
#             return todo
#     raise HTTPException(status_code=404, detail="item not found")

# create to do 
@app.post("/new/")
def create_todo(request: Todo, session: SessionDep):
    new_todo_id = str(uuid4())
    created = datetime.now()

    new_todo = todos(
        id = new_todo_id,
        title = request.title,
        description = request.description,
        completed = request.completed,
        date_created = created,
        priority= request.priority
     )
    
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)

    return "successfully added todo"


        
# # edit to do
# @api.put("/update/{id}")
# def edit_todo(id: int, todo: TodoUpdate):
#     for index, to_do in enumerate(all_todos):
#         if id == index:
#             to_do.name = todo.name,
#             to_do.description = todo.description    
        
#             return {"message": f"Successfully updated todo with id: {id} ",
#                     "data": to_do}
#     return "Could not update"

# # delete to do

# @api.delete("/drop/{id}")
# def delete_todo(id: int):
#     for index, todo_item in enumerate(all_todos):
#         if id == index:
#             all_todos.pop(index)

#             return{"message": f"Successfully deleted todo item number {id}"}
