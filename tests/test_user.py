import json
import pytest
from main import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_user(client):
    payload = {"username": "alice", "email": "alice@example.com"}
    response = client.post("/users", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "houses" in data
    assert "rooms" in data

def test_get_users(client):
    # Create a user first
    payload = {"username": "bob", "email": "bob@example.com"}
    client.post("/users", data=json.dumps(payload), content_type="application/json")
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(user["username"] == "bob" for user in data)
