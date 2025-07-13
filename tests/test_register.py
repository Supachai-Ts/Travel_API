from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_register_user():
    
    res = client.post("/register/", json={
        "username": "test_register_user",
        "password": "secure_password123"
    })
    assert res.status_code == 200

    data = res.json()
    assert "id" in data
    assert data["username"] == "test_register_user"
