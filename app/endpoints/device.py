# app/endpoints/device.py
from flask import Blueprint, request, jsonify
from app.endpoints.user import USERS          
from app.endpoints.house import HOUSES          
from app.endpoints.room import ROOMS            

device_bp = Blueprint('device_bp', __name__)

# In-memory store for devices.
# We use a compound key: "house_address:room_name:device_name"
DEVICES = {}

@device_bp.route('/devices', methods=['POST'])
def create_device():
    """
    Create a new device.
    Required JSON fields:
      - 'user_id': Owner of the device.
      - 'house_address': Address of the house where the device is located.
      - 'room_name': Name of the room where the device is located.
      - 'device_name': Name/identifier of the device.
      - 'device_type': Type/category of the device.
    
    Updates the room's record to include the new device.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    house_address = data.get('house_address')
    room_name = data.get('room_name')
    device_name = data.get('device_name')
    device_type = data.get('device_type')
    
    if not all([user_id, house_address, room_name, device_name, device_type]):
        return jsonify({"error": "user_id, house_address, room_name, device_name, and device_type are required"}), 400

    if user_id not in USERS:
        return jsonify({"error": "User not found"}), 404
    if house_address not in HOUSES:
        return jsonify({"error": "House not found"}), 404

    room_key = f"{house_address}:{room_name}"
    if room_key not in ROOMS:
        return jsonify({"error": "Room not found"}), 404

    device_key = f"{room_key}:{device_name}"
    if device_key in DEVICES:
        return jsonify({"error": "Device already exists in this room"}), 400

    new_device = {
        "device_name": device_name,
        "device_type": device_type,
        "user_id": user_id,
        "house_address": house_address,
        "room_name": room_name
    }
    DEVICES[device_key] = new_device
    
    ROOMS[room_key].setdefault("devices", []).append(device_name)

    return jsonify(new_device), 201

@device_bp.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(list(DEVICES.values())), 200

@device_bp.route('/devices/<string:house_address>/<string:room_name>/<string:device_name>', methods=['GET'])
def get_device_details(house_address, room_name, device_name):
    """
    Retrieve details for a device identified by house address, room name, and device name.
    """
    device_key = f"{house_address}:{room_name}:{device_name}"
    device = DEVICES.get(device_key)
    if not device:
        return jsonify({"error": "Device not found"}), 404
    return jsonify(device), 200
