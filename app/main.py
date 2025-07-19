from fastapi import FastAPI
from db.models import Base
from db.db_con import engine

from routers import auth, todos


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)