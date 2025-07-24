
#from uuid import uuid4
from fastapi import APIRouter, HTTPException, Query, Path, Depends
from schemas.todos_schema import *
from db.models import todos
from db.db_con import SessionDep
from typing import Annotated
from utils import UserDep

from starlette import status
from sqlalchemy import select

router = APIRouter(
    prefix="/todos",
    tags = ["todos"]
)

#** FIX THE RESPONSE MODEL OF THE GET ALL CLASS
@router.get("/")
async def get_todos(session: SessionDep, user: UserDep, 
              limit: int = Annotated[int, Query(le=100)],  
              offset: int = 0
              ):
    #sql alchemy < 1.4 syntax
    #todos_list = session.query(todos).limit(limit).offset(offset)

    #sqlalchemy 2.0 recommended syntax
    role = user.get("role")
    if role == 1:
        stmt = select(todos).limit(limit).offset(offset)
        todos_list = session.scalars(stmt).all()
    
    if role == 2:
        stmt = select(todos).where(todos.user_id == user.get("id")).limit(limit).offset(offset)
        todos_list = session.scalars(stmt).all() 
    
    if not todos_list:
        raise HTTPException(status_code=404, detail="items not found")
    return todos_list    
    

@router.get("/{id}", status_code=status.HTTP_200_OK )
async def get_todo(id: Annotated[int, Path(gt=0)],
                   user: UserDep,  
                   session: SessionDep):

    #sql alchemy 2.0 alternative syntax for searching for primary keys
    # todo = session.get(todos, id)

    # #sql alchemy 1.4 syntax
    todo = session.query(todos).filter(todos.id == id and todos.user_id == user.get()).first()
    if not todo:
        raise HTTPException(status_code=404, detail="todo item not found")
    return todo

    #Alternative code using the select statement
    # stmt = select(todos).where(todos.id == id)
    # if not row:
    #     raise HTTPException(status_code=404, detail="item not found")
    # for row in session.scalars(stmt):
    #     return row

        
# create to do 
@router.post("/new/", status_code= status.HTTP_200_OK)
async def create_todo(request: TodoCreate, user: UserDep, session: SessionDep):
    print(request.title)
    print(user.get("id"))
    new_todo = todos(
        title = request.title,
        description = request.description,
        completed = request.completed, 
        priority = request.priority, 
        date_created = datetime.now(),
        user_id = user.get("id")
     )
    
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)

     
#  edit to do
@router.patch("/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(id: Annotated[int, Path(gt=0)],
                      user: UserDep, 
                      request: TodoUpdate, 
                      session: SessionDep):
    #todo_update = request.model_dump(exclude_unset= True)
    #Alternative way to select records
    stmt = select(todos).where(todos.id == id and user.get('id') ==todos.user_id)

    #todo item retrieved from database
    todo_db = session.scalars(stmt).one()
    if not todo_db:
        HTTPException(status_code=404, detail="todo item not found")
    
    #Optimize this code section to make the update more flexible
    # todo_db = todo_update

    todo_db.title =  request.title
    todo_db.description = request.description
    todo_db.completed = request.completed
    todo_db.priority = request.priority

    session.commit()


# delete to do

@router.delete("/drop/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: Annotated[int, Path(gt=0)],
                      user: UserDep, 
                      session: SessionDep):
    #todo_db = session.get(todos, id)

    role = user.get("role")
    if role == 1:
        stmt = select(todos).where(todos.id == id)
        todo_db = session.scalars(stmt).one()
    
    if role == 2:
        stmt = stmt = select(todos).where(todos.id == id and todos.user_id == user.get('id'))
        todo_db = session.scalars(stmt).one()

    stmt = select(todos).where(todos.id == id and todos.user_id == user.get('id'))
    todo_db = session.scalars(stmt).one()

    if not todo_db:
        HTTPException(status_code=404, detail="todo item not found")
    session.delete(todo_db)
    session.commit()

    return {"message": f"Successfully deleted todo with id: {id} "}