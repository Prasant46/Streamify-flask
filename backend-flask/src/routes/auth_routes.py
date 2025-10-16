from flask import Blueprint, request
from src.controllers.auth_controller import (
    signup_controller,
    login_controller,
    logout_controller,
    onboard_controller
)
from src.middleware.auth_middleware import jwt_required_custom

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return signup_controller(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_controller(data)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return logout_controller()

@auth_bp.route('/onboarding', methods=['POST'])
@jwt_required_custom
def onboard(current_user):
    data = request.get_json()
    return onboard_controller(data, current_user)

@auth_bp.route('/me', methods=['GET'])
@jwt_required_custom
def get_current_user(current_user):
    from flask import jsonify
    return jsonify({
        'success': True,
        'user': current_user.to_dict(include_email=True)
    }), 200