from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_province():
    client.post("/register/", json={"username": "Testuser", "password": "Testpass", "firstname": "Testfirst", "lastname": "Testlast", "age": 30})
    login_res = client.post("/auth/login", data={"username": "Testuser", "password": "Testpass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/province/", json={"name": "Bangkok", "is_secondary": False}, headers=headers)
    assert res.status_code == 200
    province = res.json()
    assert province["name"] == "Bangkok"
    assert province["is_secondary"] is False
    province_id = province["id"]

    res = client.get("/province/", headers=headers)
    assert res.status_code == 200
    provinces = res.json()
    assert any(p["id"] == province_id for p in provinces)

    res = client.put(f"/province/{province_id}", json={"name": "Bangkok Updated", "is_secondary": True}, headers=headers)
    assert res.status_code == 200
    updated = res.json()
    assert updated["name"] == "Bangkok Updated"
    assert updated["is_secondary"] is True

    res = client.delete(f"/province/{province_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True

    res = client.get("/province/", headers=headers)
    assert all(p["id"] != province_id for p in res.json())
