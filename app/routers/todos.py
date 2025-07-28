
#from uuid import uuid4
from fastapi import APIRouter, HTTPException, Path, Request
from schemas.todos_schema import *
from db.models import todos
from db.db_con import SessionDep
from typing import Annotated
from utils import *

from starlette import status
from sqlalchemy import select

router = APIRouter(
    prefix="/todos",
    tags = ["todos"]
)

#Fake values to seed the database with
todo_list = [
    {
        "user_id": 2,
        "title": "Morning Workout",
        "description": "30-minute cardio session and stretching",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 1,
        "title": "Grocery Shopping",
        "description": "Buy fruits, vegetables, and other weekly supplies",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 3,
        "title": "Reply to Emails",
        "description": "Respond to work and university-related emails",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 1,
        "title": "Team Meeting",
        "description": "Attend the 11 AM team stand-up call",
        "completed": False,
        "priority": 1
    },
    {
        "user_id": 2,
        "title": "Submit Assignment",
        "description": "Upload final version of AI coursework",
        "completed": False,
        "priority": 1
    },
    {
        "user_id": 3,
        "title": "Cook Lunch",
        "description": "Prepare a healthy home-cooked meal",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 1,
        "title": "Watch Tutorial",
        "description": "Complete lesson 3 of Azure Data Factory course",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 2,
        "title": "Read Book",
        "description": "Read at least 20 pages of a personal development book",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 3,
        "title": "Plan Social Media",
        "description": "Draft next week's content for Briton and Kay Instagram",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 1,
        "title": "Test POS App",
        "description": "Run tests on the latest update of the POS system",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 2,
        "title": "Laundry",
        "description": "Wash and fold clothes",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 3,
        "title": "Backup Files",
        "description": "Backup project files to Google Drive",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 2,
        "title": "Call Parents",
        "description": "Have a 15-minute catch-up call with family",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 1,
        "title": "Clean Workspace",
        "description": "Organize desk and remove clutter",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 3,
        "title": "Meditate",
        "description": "Do a 10-minute guided meditation",
        "completed": False,
        "priority": 3
    },
    {
        "user_id": 2,
        "title": "Check KPIs",
        "description": "Review weekly business performance metrics",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 1,
        "title": "Update Portfolio",
        "description": "Add recent AI/Data Science projects to portfolio",
        "completed": False,
        "priority": 2
    },
    {
        "user_id": 3,
        "title": "Design Dashboard",
        "description": "Prototype a new Power BI sales dashboard",
        "completed": False,
        "priority": 1
    },
    {
        "user_id": 1,
        "title": "Fix Bug",
        "description": "Debug error in sales inventory pipeline",
        "completed": False,
        "priority": 1
    },
    {
        "user_id": 2,
        "title": "Research Funding",
        "description": "Look into AI-related startup grants in the UK",
        "completed": False,
        "priority": 3
    }
]

### PAGES ###
#show todos page
@router.get("/todo-page")
async def render_todos_page(request: Request, session: SessionDep):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        print(f"user: {user}")
        
        if user is None:
            print("user is None")
            return login_redirection()
        
        #To give the admin the power to view all todos
        # role = user.get("role")
        # if role == 1:
        #     stmt = select(todos)#.limit(limit).offset(offset)
        #     todos_list = session.scalars(stmt).all()
        
        # if role == 2:
        #     stmt = select(todos).where(todos.user_id == user.get("id"))#.limit(limit).offset(offset)
        #     todos_list = session.scalars(stmt).all() 
        stmt = select(todos).where(todos.user_id == user.get("id"))#.limit(limit).offset(offset)
        todos_list = session.scalars(stmt).all() 

        return templates.TemplateResponse("todos.html", {"request":request, 
                                                          "todos": todos_list,
                                                          "user": user})
    except:
        return login_redirection()

@router.get("/new-todo")
async def render_new_todo(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return login_redirection()

        return templates.TemplateResponse("new-todo.html", {"request": request, "user":user})

    except:
        return login_redirection()

@router.get("/edit-todo/{id}")
async def render_edit_todo_page(request: Request, id: Annotated[int, Path(gt=0)], session: SessionDep):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        todo = session.get(todos, id)

        if user is None:
            return login_redirection()
        
        return templates.TemplateResponse("edit-todo.html", {"request": request, "user": user, "todo": todo})

    except:
        return login_redirection()

### ENDPOINTS ###

#end point to test todos auth
# @router.get("/healthy", status_code= status.HTTP_200_OK)
# async def check_app_con():
#     return {"status":"app is healthy"}

#** FIX THE RESPONSE MODEL OF THE GET ALL CLASS
@router.get("/")
async def get_todos(session: SessionDep, user: UserDep, 
            #   limit: int = Annotated[int, Query(le=100)],  
            #   offset: int = 0
              ):
    #sql alchemy < 1.4 syntax
    todos_list = session.query(todos)#.limit(limit).offset(offset)

    #sqlalchemy 2.0 recommended syntax
    role = user.get("role")
    if role == 1:
        stmt = select(todos)#.limit(limit).offset(offset)
        todos_list = session.scalars(stmt).all()
    
    if role == 2:
        stmt = select(todos).where(todos.user_id == user.get("id"))#.limit(limit).offset(offset)
        todos_list = session.scalars(stmt).all() 
    
    if not todos_list:
        raise HTTPException(status_code=404, detail="items not found")
    
    #print(todos_list)
    return todos_list    
    #return {"status":"ok"}
    

@router.get("/todo/{id}", status_code=status.HTTP_200_OK )
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
@router.post("/add-todo", status_code= status.HTTP_201_CREATED)
async def create_todo(request: TodoCreate, user: UserDep, session: SessionDep):
    # print(request.title)
    # print(user.get("id"))
    new_todo = todos(
        title = request.title,
        description = request.description,
        completed = request.completed, 
        priority = request.priority, 
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

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
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




### GENERATE TODOS DATA ###3
def add_todos(todo_list_obj, session: SessionDep):
    for todo in todo_list_obj:
        new_todo = todos(
        title = todo["title"],
        description = todo["description"],
        completed = todo["completed"], 
        priority = todo["priority"], 
        user_id = todo["user_id"]
     )
        #print(new_todo)
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)

@router.get("/generate", status_code=status.HTTP_201_CREATED)
async def generate_todos(session: SessionDep):
    add_todos(todo_list, session)
    return "Generated successfully"