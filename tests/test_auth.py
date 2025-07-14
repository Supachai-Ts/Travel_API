from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_login_success():
    client.post("/register/", json={"username": "Testuser", "password": "Testpass", "firstname": "Testfirst", "lastname": "Testlast", "age": 30})
    
    res = client.post("/auth/login", data={"username": "Testuser", "password": "Testpass"})
    token = res.json()["access_token"]
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
