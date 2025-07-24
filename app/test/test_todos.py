#from typing import Annotated
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker # Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from utils import Roles, get_current_user
from main import app
from db.db_con import get_session
from db.models import Base, todos


#define database URL
SQL_DB_URL = "sqlite:///test_todoapp.db"

#define engine 
engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

#define local session
TestSessionLocal =  sessionmaker(autoflush=False, autocommit =False, bind=engine)

Base.metadata.create_all(bind=engine)

#create dependency function 
def override_get_session():
    with TestSessionLocal() as test_session:
        yield test_session

def override_get_current_user():
    return {"username" : "Kessy", "id":1, "user_role": "ADMIN"}

#overriding dependencies
app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_current_user] = override_get_current_user

# TestSessionDep = Annotated[Session, Depends(test_get_session)]

#Define Declarative base


# #Create todos model

# class test_user(Base):
#     __tablename__ = "test_users"

#     id: Mapped[int] = mapped_column(primary_key=True, index = True)
#     email: Mapped[str] = mapped_column(unique=True)
#     username: Mapped[str] = mapped_column(unique=True)
#     first_name: Mapped[str]
#     last_name: Mapped[str]
#     hashed_password: Mapped[str] = mapped_column(unique= True)
#     is_active: Mapped[bool] = mapped_column(default=True)
#     role: Mapped[Roles] 

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = todos(
        title="Design Dashboard",
        description="Prototype a new Power BI sales dashboard",
        completed= False,
        priority=1
    )

    db = TestSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as conn:
        conn.execute(text("DELETE * FROM todos"))
        conn.commit()

def test_autheticate_read_all(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json == {"title" : "Design Dashboard",
        "description" : "Prototype a new Power BI sales dashboard",
        "completed" : False,
        "priority" : 1}

