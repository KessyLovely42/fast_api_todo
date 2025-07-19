from fastapi import FastAPI
from db.models import Base
from db.db_con import engine

from routers import auth, todos, admin, users


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)