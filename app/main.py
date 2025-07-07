from uuid import uuid4
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from db.schemas import *
from db.models import Base, todos
from db.db_con import engine, SessionDep
from datetime import datetime
from typing import Annotated

from sqlalchemy import select


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/todos", response_model= List[Todo])
def get_todos(session: SessionDep, 
              limit: int = Annotated[int, Query(le=100)],  
              offset: int = 0
              ):
    stmt = select(todos).limit(limit).offset(offset)
    todos_list = session.scalars(stmt).all()
    if todos_list:
        return todos_list
    else:
        raise HTTPException(status_code=404, detail="items not found")
    

@app.get("/todo/{id}", response_model= Todo)
def get_todo(id: int, session: SessionDep):
    todo = session.get(todos, id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo item not found")
    return todo

    #Alternative code using the select statement
    # stmt = select(todos).where(todos.id == id)
    # for row in session.scalars(stmt):
    #     if not row:
    #         raise HTTPException(status_code=404, detail="item not found")
    #     return row

    

        
# create to do 
@app.post("/new/")
def create_todo(request: TodoCreate, session: SessionDep):
    created = datetime.now()

    new_todo = todos(
        #id = new_todo_id,
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


        
#  edit to do
@app.patch("/update/{id}")
def update_todo(id: int, request: TodoUpdate, session: SessionDep):
    todo_update = request.model_dump(exclude_unset= True)

    todo_db = session.get(todos, id)
    #Alternative way to select records
    # stmt = select(todos).where(todos.id == id)

    #todo item retrieved from database
    # todo_db = session.scalars(stmt).one()
    if not todo_db:
        HTTPException(status_code=404, detail="todo item not found")
    
    #Optimize this code section to make the update more flexible
    todo_db.title =  request.title
    todo_db.description = request.description
    todo_db.completed = request.completed
    todo_db.priority = request.priority

    session.commit()

    

        
    return {"message": f"Successfully updated todo with id: {id} ",
            "data": todo_update}


# delete to do

@app.delete("/drop/{id}")
def delete_todo(id: int, session: SessionDep):
    todo_db = session.get(todos, id)
    if not todo_db:
        HTTPException(status_code=404, detail="todo item not found")
    session.delete(todo_db)
    session.commit()

    return {"message": f"Successfully deleted todo with id: {id} "}