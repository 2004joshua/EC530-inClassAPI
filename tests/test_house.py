import json
import pytest
from main import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_house(client):
    # Create a user first
    user_payload = {"username": "charlie", "email": "charlie@example.com"}
    user_resp = client.post("/users", data=json.dumps(user_payload), content_type="application/json")
    user_data = user_resp.get_json()
    user_id = user_data["id"]

    house_payload = {"address": "123 Main St", "user_id": user_id, "floors": 2}
    response = client.post("/houses", data=json.dumps(house_payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert data["address"] == "123 Main St"
    assert data["floors"] == 2
    assert data["room_count"] == 0

def test_get_house_details(client):
    # Create a user and house
    user_payload = {"username": "dave", "email": "dave@example.com"}
    user_resp = client.post("/users", data=json.dumps(user_payload), content_type="application/json")
    user_id = user_resp.get_json()["id"]

    house_payload = {"address": "456 Elm St", "user_id": user_id, "floors": 1}
    client.post("/houses", data=json.dumps(house_payload), content_type="application/json")
    response = client.get("/houses/456 Elm St")
    assert response.status_code == 200
    data = response.get_json()
    assert data["address"] == "456 Elm St"
    assert data["floors"] == 1
    assert "owner" in data
    assert data["owner"]["username"] == "dave"
