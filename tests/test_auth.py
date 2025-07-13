from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_login_success():
    client.post("/register/", json={"username":"u1","password":"p1"})
    res = client.post("/auth/login", params={"username":"u1","password":"p1"})
    assert res.status_code == 200
    assert "access_token" in res.json()
