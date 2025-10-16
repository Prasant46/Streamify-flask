from flask import jsonify, current_app
from src.utils.stream import generate_stream_token

def get_stream_token_controller(current_user):
  """Generate Stream token for authenticated user"""
  try:
    token = generate_stream_token(current_user.id)
    
    if not token:
      return jsonify({"success": False, "msg": "Failed to generate Stream token"}), 500
    
    return jsonify({
            'success': True,
            'token': token,
            'apiKey': current_app.config.get('STREAM_API_KEY'),
            'userId': str(current_user.id)
        }), 200
    
  except Exception as e:
    return jsonify({"success": False, "msg": f"Internal server error: {str(e)}"}), 500
    
    