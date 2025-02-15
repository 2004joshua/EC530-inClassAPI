# app/endpoints/house.py
from flask import Blueprint, request, jsonify
from app.endpoints.user import USERS  # Import the USERS dictionary

house_bp = Blueprint('house_bp', __name__)

# In-memory store for houses; using the house address as the key.
HOUSES = {}

@house_bp.route('/houses', methods=['POST'])
def create_house():
    """
    Create a new house.
    Required JSON fields: 'address', 'user_id'
    Optional JSON field: 'floors' (defaults to 1 if not provided)
    
    Updates the owner's record (in USERS) with the new house address.
    Initializes 'room_count' to 0 and an empty 'rooms' list.
    """
    data = request.get_json()
    address = data.get('address')
    user_id = data.get('user_id')
    floors = data.get('floors', 1)  # default to 1 floor if not provided

    if not address or not user_id:
        return jsonify({"error": "Address and user_id are required"}), 400

    if user_id not in USERS:
        return jsonify({"error": "User not found"}), 404

    if address in HOUSES:
        return jsonify({"error": "House already exists with this address"}), 400

    new_house = {
        "address": address,
        "user_id": user_id,
        "floors": floors,
        "room_count": 0,   # no rooms initially
        "rooms": []        # list to store room names
    }
    HOUSES[address] = new_house

    # Update the user record with the new house.
    USERS[user_id].setdefault("houses", []).append(address)
    return jsonify(new_house), 201

@house_bp.route('/houses', methods=['GET'])
def get_houses():
    return jsonify(list(HOUSES.values())), 200

@house_bp.route('/houses/<string:address>', methods=['GET'])
def get_house_details(address):
    """
    Retrieve detailed information for a house by address.
    Returns house details including floors, room_count, room names, and owner info.
    """
    house = HOUSES.get(address)
    if not house:
        return jsonify({"error": "House not found"}), 404

    user_id = house["user_id"]
    owner = USERS.get(user_id, {})
    response = {
        "address": house["address"],
        "floors": house.get("floors"),
        "room_count": house.get("room_count", 0),
        "rooms": house.get("rooms", []),
        "owner": {
            "username": owner.get("username"),
            "email": owner.get("email")
        }
    }
    return jsonify(response), 200
