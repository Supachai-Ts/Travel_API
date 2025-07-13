from fastapi.testclient import TestClient
from tralvel_app.main import app

client = TestClient(app)

def test_food():
    res = client.post("/food/", json={"name": "Pad Thai", "price": 80.0})
    assert res.status_code == 200
    food = res.json()
    assert food["name"] == "Pad Thai"
    assert food["price"] == 80.0
    food_id = food["id"]

    res = client.get("/food/")
    assert res.status_code == 200
    foods = res.json()
    assert any(f["id"] == food_id for f in foods)

    res = client.put(f"/food/{food_id}", json={"name": "Pad See Ew", "price": 90.0})
    assert res.status_code == 200
    updated = res.json()
    assert updated["name"] == "Pad See Ew"
    assert updated["price"] == 90.0

    res = client.delete(f"/food/{food_id}")
    assert res.status_code == 200
    msg = res.json()
    assert msg["ok"] is True
    assert f"{food_id}" in msg["message"]

    res = client.get("/food/")
    assert all(f["id"] != food_id for f in res.json())
