from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.models.user import User

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"message": "Missing or invalid token"}), 401
            # Convert string ID back to integer for database query
            user = User.query.get(int(user_id))
            if not user:
                return jsonify({"message": "User not found"}), 404
            # Pass user as current_user to the route
            kwargs['current_user'] = user
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": f"Unauthorized: {str(e)}"}), 401
    return wrapper