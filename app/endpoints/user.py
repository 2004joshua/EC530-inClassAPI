# app/endpoints/user.py
from flask import Blueprint, request, jsonify

user_bp = Blueprint('user_bp', __name__)

# In-memory store for users; keys are numeric user IDs.
USERS = {}
CURRENT_USERID = 0

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    Required JSON fields: 'username', 'email'
    """
    global CURRENT_USERID
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400
  
    CURRENT_USERID += 1
    USERS[CURRENT_USERID] = {
        "id": CURRENT_USERID, 
        "username": username,
        "email": email,
        "houses": [],  # list of house addresses the user owns
        "rooms": []    # list of room names the user owns
    }
    return jsonify(USERS[CURRENT_USERID]), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(USERS.values())), 200
