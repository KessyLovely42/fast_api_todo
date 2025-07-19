from fastapi import Depends
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, declarative_base

SQL_DATABASE_URL = "sqlite:///todoapp.db"

engine = create_engine(SQL_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit =False, bind = engine)

#sql alchemy 2.0 version alternative
class Base(DeclarativeBase):
    pass

#sql alchemy < 1.4 version
# Base = declarative_base()

# async def create_db_and_tables():
#     await Base.metadata.create_all(engine)

async def get_session():
    with SessionLocal() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
    




