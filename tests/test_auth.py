from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_login_success():
    client.post("/register/", json={
        "username": "Testuser",
        "password": "Testpass",
        "firstname": "Testfirst",
        "lastname": "Testlast",
        "age": 30
    })
    res = client.post("/auth/login", params={"username":"Testuser","password":"Testpass"})
    assert res.status_code == 200
    assert "access_token" in res.json()
