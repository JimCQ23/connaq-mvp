from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_success():
    payload = {
        "FIRST_NAME": "Rock",
        "USERNAME": "Rock123",
        "EMAIL": "Rock@example.com",
        "PASSWORD": "secretpass"
    }
    
    response = client.post("/api/users/", json=payload)
    assert response.status_code == 200  # 200 OK for success
    data = response.json()
    assert "USER_ID" in data
    assert data["FIRST_NAME"] == "Rock"
    assert data["USERNAME"] == "Rock123"
    assert data["EMAIL"] == "Rock@example.com"

def test_create_user_duplicate_email():
    payload = {
        "FIRST_NAME": "Rock",
        "USERNAME": "Rock123",
        "EMAIL": "Rock@example.com",  # Same email as previous test
        "PASSWORD": "secretpass"
    }
    
    response = client.post("/api/users/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"
