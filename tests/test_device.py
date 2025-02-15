import json
import pytest
from main import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_device(client):
    # Create user, house, and room first
    user_payload = {"username": "gina", "email": "gina@example.com"}
    user_resp = client.post("/users", data=json.dumps(user_payload), content_type="application/json")
    user_id = user_resp.get_json()["id"]

    house_payload = {"address": "202 Maple St", "user_id": user_id, "floors": 1}
    client.post("/houses", data=json.dumps(house_payload), content_type="application/json")

    room_payload = {
        "house_address": "202 Maple St",
        "user_id": user_id,
        "floor": 1,
        "room_name": "Kitchen",
        "room_type": "Utility"
    }
    client.post("/rooms", data=json.dumps(room_payload), content_type="application/json")

    device_payload = {
        "user_id": user_id,
        "house_address": "202 Maple St",
        "room_name": "Kitchen",
        "device_name": "Fridge",
        "device_type": "Appliance"
    }
    device_resp = client.post("/devices", data=json.dumps(device_payload), content_type="application/json")
    assert device_resp.status_code == 201
    device_data = device_resp.get_json()
    assert device_data["device_name"] == "Fridge"
    assert device_data["device_type"] == "Appliance"

def test_get_device_details(client):
    # Create the required user, house, room, then device
    user_payload = {"username": "henry", "email": "henry@example.com"}
    user_resp = client.post("/users", data=json.dumps(user_payload), content_type="application/json")
    user_id = user_resp.get_json()["id"]

    house_payload = {"address": "303 Birch St", "user_id": user_id, "floors": 2}
    client.post("/houses", data=json.dumps(house_payload), content_type="application/json")

    room_payload = {
        "house_address": "303 Birch St",
        "user_id": user_id,
        "floor": 1,
        "room_name": "Bedroom",
        "room_type": "Private"
    }
    client.post("/rooms", data=json.dumps(room_payload), content_type="application/json")

    device_payload = {
        "user_id": user_id,
        "house_address": "303 Birch St",
        "room_name": "Bedroom",
        "device_name": "Lamp",
        "device_type": "Lighting"
    }
    client.post("/devices", data=json.dumps(device_payload), content_type="application/json")

    response = client.get("/devices/303 Birch St/Bedroom/Lamp")
    assert response.status_code == 200
    device_data = response.get_json()
    assert device_data["device_name"] == "Lamp"
