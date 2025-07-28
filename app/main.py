from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from db.models import Base
from db.db_con import engine

from routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

#endpoint for testing
# @app.get("/healthy")
# async def check_app_con():
#     return {"status":"app is healthy"}

#endpoint to check the home html
@app.get("/")
async def view_check(request: Request):
    return RedirectResponse("/todos/todo-page")

app.include_router(admin.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)