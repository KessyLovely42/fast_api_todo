#from typing import Annotated
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from utils import Roles, get_current_user
from main import app
from db.db_con import get_session
from test.utils import *

#create dependency function 
def override_get_session():
    with TestSessionLocal() as test_session:
        yield test_session

def override_get_current_user():
    return {"username" : "Kessy", "id":1, "user_role": "ADMIN"}

#overriding dependencies
app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_todos_check_if_healthy():
    response = client.get("/todos/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status":"app is healthy"}

def test_get_all_todos(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response == [{
        "id": 1,
        "title" : "Design Dashboard",
        "description" : "Prototype a new Power BI sales dashboard",
        "completed" : False,
        "date_created": "2025-07-25 10:37:08.526165",
        "priority" : 1,
        "user_id": 1}]

def test_get_one_todos(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title" : "Design Dashboard",
        "description" : "Prototype a new Power BI sales dashboard",
        "completed" : False,
        "date_created": "2025-07-25 10:37:08.526165",
        "priority" : 1,
        "user_id": 1}

def test_get_one_todo_failed(test_todo):
    response = client.get("/todos/todo/898")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_todo():
    todo_request = {
        "title": "Design Dashboard",
        "description": "Prototype a new Power BI sales dashboard",
        "completed": False,
        "priority": 1
    }

    response = client.post("/todos/new/", json = todo_request)
    assert response.status_code == status.HTTP_201_CREATED