from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_user():

    res = client.get("/users/")
    assert res.status_code == 200
    users = res.json()
    assert len(users) > 0, "ต้องมีผู้ใช้อย่างน้อย 1 คนในระบบก่อนทดสอบ"
    user_id = users[0]["id"]

    updated_data = {
        "username": "Testuser",
        "password": "Testpass",
        "firstname": "Testfirst",
        "lastname": "Testlast",
        "age": 30
    }

    res = client.put(f"/users/{user_id}", json=updated_data)
    assert res.status_code == 200
    updated = res.json()
    assert updated["username"] == updated_data["username"]
    assert updated["password"] == updated_data["password"]
    assert updated["firstname"] == updated_data["firstname"]
    assert updated["lastname"] == updated_data["lastname"]
    assert updated["age"] == updated_data["age"]

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    deleted = res.json()
    assert deleted["id"] == user_id

    res = client.get("/users/")
    assert all(u["id"] != user_id for u in res.json())
