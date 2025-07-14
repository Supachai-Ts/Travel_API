from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_user():
    client.post("/register/", json={"username": "Testuser", "password": "Testpass", "firstname": "Testfirst", "lastname": "Testlast", "age": 30})
    login_res = client.post("/auth/login", data={"username": "Testuser", "password": "Testpass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/users/", headers=headers)
    assert res.status_code == 200
    users = res.json()
    assert len(users) > 0, "ต้องมีผู้ใช้อย่างน้อย 1 คนในระบบก่อนทดสอบ"
    user_id = users[0]["id"]

    updated_data = {"username": "Testuser", "password": "Testpass", "firstname": "Testfirst", "lastname": "Testlast", "age": 30}

    res = client.put(f"/users/{user_id}", json=updated_data, headers=headers)
    assert res.status_code == 200
    updated = res.json()
    assert updated["username"] == updated_data["username"]
    assert updated["password"] == updated_data["password"]
    assert updated["firstname"] == updated_data["firstname"]
    assert updated["lastname"] == updated_data["lastname"]
    assert updated["age"] == updated_data["age"]

    res = client.delete(f"/users/{user_id}", headers=headers)
    assert res.status_code == 200
    deleted = res.json()
    assert deleted["id"] == user_id

    res = client.get("/users/", headers=headers)
    assert all(u["id"] != user_id for u in res.json())
