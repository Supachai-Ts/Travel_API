from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_user_crud_only_get_put_delete():

    res = client.get("/users/")
    assert res.status_code == 200
    users = res.json()
    assert len(users) > 0, "ต้องมีผู้ใช้อย่างน้อย 1 คนในระบบก่อนทดสอบ"
    user_id = users[0]["id"]

    res = client.put(f"/users/{user_id}", json={"username": "patched_user", "password": "patched_pass"})
    assert res.status_code == 200
    updated = res.json()
    assert updated["username"] == "patched_user"

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    deleted = res.json()
    assert deleted["id"] == user_id

    res = client.get("/users/")
    assert all(u["id"] != user_id for u in res.json())
