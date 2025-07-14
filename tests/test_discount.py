from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_discount_per_province():
    client.post("/register/", json={"username": "Testuser", "password": "Testpass", "firstname": "Testfirst", "lastname": "Testlast", "age": 30})
    login_res = client.post("/auth/login", data={ "username": "Testuser", "password": "Testpass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/province/", json={"name": "Bangkok", "is_secondary": False},headers=headers)
    client.post("/province/", json={"name": "Chiang Rai", "is_secondary": True},headers=headers)

    client.post("/food/", json={"name": "Pad Thai", "price": 100.0})
    client.post("/food/", json={"name": "Pad See Ew", "price": 80.0})

    res = client.get("/discount/", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert "Bangkok" in data
    assert "Chiang Rai" in data

    bangkok = data["Bangkok"]
    assert any(f["food"] == "Pad Thai" and f["discounted_price"] == 50.0 for f in bangkok)
    assert any(f["food"] == "Pad See Ew" and f["discounted_price"] == 40.0 for f in bangkok)

    chiangrai = data["Chiang Rai"]
    assert any(f["food"] == "Pad Thai" and f["discounted_price"] == 40.0 for f in chiangrai)
    assert any(f["food"] == "Pad See Ew" and f["discounted_price"] == 32.0 for f in chiangrai)
