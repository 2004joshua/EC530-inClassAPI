import json
import pytest
from main import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_room(client):
    # Create user and house first
    user_payload = {"username": "eve", "email": "eve@example.com"}
    user_resp = client.post("/users", data=json.dumps(user_payload), content_type="application/json")
    user_id = user_resp.get_json()["id"]

    house_payload = {"address": "789 Oak St", "user_id": user_id, "floors": 1}
    client.post("/houses", data=json.dumps(house_payload), content_type="application/json")

    room_payload = {
        "house_address": "789 Oak St",
        "user_id": user_id,
        "floor": 1,
        "room_name": "Living Room",
        "room_type": "Common"
    }
    room_resp = client.post("/rooms", data=json.dumps(room_payload), content_type="application/json")
    assert room_resp.status_code == 201
    room_data = room_resp.get_json()
    assert room_data["room_name"] == "Living Room"
    assert room_data["room_type"] == "Common"
    assert room_data["floor"] == 1

def test_get_room_details(client):
    # Create user, house, and room
    user_payload = {"username": "frank", "email": "frank@example.com"}
    user_resp = client.post("/users", data=json.dumps(user_payload), content_type="application/json")
    user_id = user_resp.get_json()["id"]

    house_payload = {"address": "101 Pine St", "user_id": user_id, "floors": 2}
    client.post("/houses", data=json.dumps(house_payload), content_type="application/json")

    room_payload = {
        "house_address": "101 Pine St",
        "user_id": user_id,
        "floor": 2,
        "room_name": "Office",
        "room_type": "Study"
    }
    client.post("/rooms", data=json.dumps(room_payload), content_type="application/json")

    response = client.get("/rooms/101 Pine St/Office")
    assert response.status_code == 200
    room_data = response.get_json()
    assert room_data["room_name"] == "Office"
