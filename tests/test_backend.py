from fastapi.testclient import TestClient
from Backend.main import app

client = TestClient(app)

def test_creat_user():
    response = client.post("/users",
                           json={"username": "Youssef", "password": "2002"})
    assert response.status_code == 200
    date = response.json()
    assert "id" in date
    assert date["username"] == "Youssef"

def test_login_post():
    response = client.post(
        "/login",
        json={"username": "Youssef", "password": "2002"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data