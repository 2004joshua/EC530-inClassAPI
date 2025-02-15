# app/endpoints/room.py
from flask import Blueprint, request, jsonify
from app.endpoints.house import HOUSES  # Import houses dictionary
from app.endpoints.user import USERS   # Import users dictionary

room_bp = Blueprint('room_bp', __name__)

# In-memory store for rooms.
# We use a compound key: "house_address:room_name"
ROOMS = {}

@room_bp.route('/rooms', methods=['POST'])
def create_room():
    """
    Create a new room.
    Required JSON fields:
      - 'house_address': Address of the house the room belongs to.
      - 'user_id': ID of the user (should match the house owner).
      - 'floor': Floor number where the room is located.
      - 'room_name': Name of the room.
      - 'room_type': Type/category of the room.
    
    Initializes an empty 'devices' array.
    Updates both the user and the house with the room name.
    """
    data = request.get_json()
    house_address = data.get('house_address')
    user_id = data.get('user_id')
    floor = data.get('floor')
    room_name = data.get('room_name')
    room_type = data.get('room_type')

    if not all([house_address, user_id, floor, room_name, room_type]):
        return jsonify({"error": "house_address, user_id, floor, room_name, and room_type are required"}), 400

    if user_id not in USERS:
        return jsonify({"error": "User not found"}), 404
    if house_address not in HOUSES:
        return jsonify({"error": "House not found"}), 404

    # Create a compound key for uniqueness.
    key = f"{house_address}:{room_name}"
    if key in ROOMS:
        return jsonify({"error": "Room already exists in this house"}), 400

    new_room = {
        "house_address": house_address,
        "user_id": user_id,
        "floor": floor,
        "room_name": room_name,
        "room_type": room_type,
        "devices": []  # Initially, no devices.
    }
    ROOMS[key] = new_room

    # Update the user's record with this room.
    USERS[user_id].setdefault("rooms", []).append(room_name)

    # Update the house's record.
    house = HOUSES[house_address]
    house["room_count"] = house.get("room_count", 0) + 1
    house.setdefault("rooms", []).append(room_name)

    return jsonify(new_room), 201

@room_bp.route('/rooms', methods=['GET'])
def get_rooms():
    return jsonify(list(ROOMS.values())), 200

@room_bp.route('/rooms/<string:house_address>/<string:room_name>', methods=['GET'])
def get_room_details(house_address, room_name):
    """
    Retrieve details for a room identified by its house address and room name.
    """
    key = f"{house_address}:{room_name}"
    room = ROOMS.get(key)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(room), 200
