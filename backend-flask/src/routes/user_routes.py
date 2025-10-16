from flask import Blueprint, request
from src.controllers.user_controller import (
    get_all_users_controller,
    search_users_controller,
    get_user_profile_controller,
    send_friend_request_controller,
    accept_friend_request_controller,
    get_friend_requests_controller,
    get_friends_controller
)
from src.middleware.auth_middleware import jwt_required_custom

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required_custom
def get_all_users(current_user):
    return get_all_users_controller(current_user)

@user_bp.route('/search', methods=['GET'])
@jwt_required_custom
def search_users(current_user):
    query = request.args.get('q', '')
    return search_users_controller(query, current_user)

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required_custom
def get_user_profile(user_id, current_user):
    return get_user_profile_controller(user_id, current_user)

@user_bp.route('/friend-request/<int:recipient_id>', methods=['POST'])
@jwt_required_custom
def send_friend_request(recipient_id, current_user):
    return send_friend_request_controller(recipient_id, current_user)

@user_bp.route('/friend-request/<int:request_id>/accept', methods=['PUT'])
@jwt_required_custom
def accept_friend_request(request_id, current_user):
    return accept_friend_request_controller(request_id, current_user)

@user_bp.route('/friend-requests', methods=['GET'])
@jwt_required_custom
def get_friend_requests(current_user):
    return get_friend_requests_controller(current_user)

@user_bp.route('/outgoing-friend-requests', methods=['GET'])
@jwt_required_custom
def get_outgoing_friend_requests(current_user):
    from src.controllers.user_controller import get_outgoing_friend_requests_controller
    return get_outgoing_friend_requests_controller(current_user)

@user_bp.route('/friends', methods=['GET'])
@jwt_required_custom
def get_friends(current_user):
    return get_friends_controller(current_user)