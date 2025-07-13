from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_discount_per_province():
    client.post("/province/", json={"name": "Bangkok", "is_secondary": False})
    client.post("/province/", json={"name": "Chiang Rai", "is_secondary": True})

    client.post("/food/", json={"name": "Pad Thai", "price": 100.0})
    client.post("/food/", json={"name": "Pad See Ew", "price": 80.0})

    res = client.get("/discount/")
    assert res.status_code == 200
    data = res.json()

    assert "Bangkok" in data
    assert "Chiang Rai" in data

    bangkok = data["Bangkok"]
    assert any(f["food"] == "ข้าวมันไก่" and f["discounted_price"] == 50.0 for f in bangkok)
    assert any(f["food"] == "ก๋วยเตี๋ยว" and f["discounted_price"] == 40.0 for f in bangkok)

    chiangrai = data["Chiang Rai"]
    assert any(f["food"] == "ข้าวมันไก่" and f["discounted_price"] == 40.0 for f in chiangrai)
    assert any(f["food"] == "ก๋วยเตี๋ยว" and f["discounted_price"] == 32.0 for f in chiangrai)
