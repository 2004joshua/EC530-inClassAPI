# main.py
from flask import Flask
from app.endpoints.user import user_bp
from app.endpoints.house import house_bp
from app.endpoints.room import room_bp
from app.endpoints.device import device_bp

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(house_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(device_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
