from flask import Blueprint
from src.controllers.chat_controller import get_stream_token_controller
from src.middleware.auth_middleware import jwt_required_custom

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/token', methods=['GET'])
@jwt_required_custom
def get_stream_token(current_user):
    return get_stream_token_controller(current_user)