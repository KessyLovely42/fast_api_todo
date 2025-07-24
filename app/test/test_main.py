from fastapi.testclient import TestClient
import main 
from fastapi import status

client = TestClient(main.app)

def test_check_if_healthy():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status":"app is healthy"}