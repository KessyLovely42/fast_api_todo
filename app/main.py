from fastapi import FastAPI, status
from db.models import Base
from db.db_con import engine

from routers import auth, todos, admin, users


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/healthy")
async def check_if_healthy():
    return {"status":"app is healthy"}

@app.get("/", status_code= status.HTTP_200_OK)
async def get_all():
    return "endpoint okay"


app.include_router(admin.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)