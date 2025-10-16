import random
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask import jsonify, make_response, current_app
from src.extensions import db
from src.models.user import User
from src.utils.stream import upsert_stream_user
from src.utils.helpers import validate_email

def signup_controller(data):
  try:
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    full_name = data.get('fullName', '').strip()
    
    #validation
    if not all([email, password, full_name]):
      return jsonify({"message": "All fields are required"}), 400
    if len(password) < 6:
      return jsonify({"message": "Password must be at least 6 characters"}), 400
    if not validate_email(email):
      return jsonify({"message": "Invalid email format"}), 400
    
    #check existing user
    if User.query.filter_by(email=email).first():
      return jsonify({"message": "Email already registered"}), 409
    
    #Generate random avatar
    idx = random.randint(1, 100)
    random_avatar = f"https://avatar.iran.liara.run/public/{idx}.png"

    #create user
    new_user = User(
      email=email,
      full_name=full_name,
      profile_pic=random_avatar
    )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    #create stream user
    upsert_stream_user({
      "id": str(new_user.id),
      "name": new_user.full_name,
      "image": new_user.profile_pic or '',
    })
    
    #create JWT token
    access_token = create_access_token(identity=str(new_user.id))

    response = make_response(jsonify({
      "success": True,
      "user": new_user.to_dict(include_email=True)
    }), 201)
    
    # Set JWT cookie manually with correct name
    cookie_name = current_app.config.get('JWT_ACCESS_COOKIE_NAME', 'access_token_cookie')
    response.set_cookie(
      cookie_name,
      value=access_token,
      max_age=7*24*60*60,  # 7 days
      httponly=True,
      samesite='Lax',
      secure=False,
      path='/'
    )

    return response
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"Internal server error: {str(e)}"}), 500
  
def login_controller(data):
  try:
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    
    if not all([email, password]):
      return jsonify({'message': 'All fields are required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
      return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=str(user.id))
    
    response = make_response(jsonify({
      "success": True,
      "user": user.to_dict(include_email=True)
    }), 200)
    
    # Set JWT cookie manually with correct name
    cookie_name = current_app.config.get('JWT_ACCESS_COOKIE_NAME', 'access_token_cookie')
    response.set_cookie(
      cookie_name,
      value=access_token,
      max_age=7*24*60*60,  # 7 days
      httponly=True,
      samesite='Lax',
      secure=False,
      path='/'
    )
    
    return response
  except Exception as e:
    return jsonify({"message": f"Internal server error: {str(e)}"}), 500
  
def logout_controller():
  try:
    response = make_response(jsonify({"message": "Logout successful", "success": True}), 200)
    unset_jwt_cookies(response)
    return response
  except Exception as e:
    return jsonify({"message": f"Internal server error: {str(e)}"}), 500
  
def onboard_controller(data, current_user):
  try:
    required_fields = ['fullName', 'bio', 'nativeLanguage', 'learningLanguage', 'location']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
      return jsonify({
        'message': 'All fields are required',
        'missingFields': missing_fields
      }), 400
    
    current_user.full_name = data.get('fullName').strip()
    current_user.bio = data.get('bio').strip()
    current_user.native_language = data.get('nativeLanguage').strip()
    current_user.learning_language = data.get('learningLanguage').strip()
    current_user.location = data.get('location').strip()
    
    if data.get('profilePic'):
      current_user.profile_pic = data.get('profilePic').strip()
      
    current_user.is_onboarded = True
    db.session.commit()
    
    #Update Stream user
    upsert_stream_user({
      "id": str(current_user.id),
      "name": current_user.full_name,
      "image": current_user.profile_pic or '',
    })
    
    return jsonify({
      'success': True,
      'user': current_user.to_dict(include_email=True)
    }), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"Internal server error: {str(e)}"}), 500