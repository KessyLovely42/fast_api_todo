import pytest
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from db.models import todos
from db.db_con import Base
from fastapi.templating import Jinja2Templates


#define database URL
SQL_DB_URL = "sqlite:///test_todoapp.db"

#define engine 
engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

#page templatexs
templates = Jinja2Templates(directory="app/templates")

#define local session
TestSessionLocal =  sessionmaker(autoflush=False, autocommit =False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def test_todo():
    todo = todos(
        title="Design Dashboard",
        description="Prototype a new Power BI sales dashboard",
        completed= False,
        priority=1
    )
    todo.date_created = "2025-07-25 10:37:08.526165"
    todo.user_id = 1

    db = TestSessionLocal()
    db.add(todo)
    db.commit()

    #test_response = 
    #print(f"todo ============ {todo.to_dict()}")
    yield todo.to_dict()

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos"))
        conn.commit()
