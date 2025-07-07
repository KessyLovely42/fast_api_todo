from fastapi import Depends
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

SQL_DATABASE_URL = "sqlite:///todo.db"

engine = create_engine(SQL_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit =False, bind = engine)

class Base(DeclarativeBase):
    pass

# async def create_db_and_tables():
#     await Base.metadata.create_all(engine)

def get_session():
    with SessionLocal() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
    




