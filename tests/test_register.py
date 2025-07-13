from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_register_user():

    res = client.post("/register/", json={
        "firstname": "Test",
        "lastname": "User",
        "age": 25,
        "username": "test_register_user",
        "password": "secure_password123",
    })
    assert res.status_code == 200

    data = res.json()
    assert "id" in data
    assert data["firstname"] == "Test"
    assert data["lastname"] == "User"
    assert data["age"] == 25
    assert data["username"] == "test_register_user"
    assert data["password"] == "secure_password123"
