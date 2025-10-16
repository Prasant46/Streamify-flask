from flask import jsonify
from sqlalchemy import or_, and_
from src.extensions import db
from src.models.user import User, Friendship
from src.models.friend_request import FriendRequest

def get_all_users_controller(current_user):
    """Get all onboarded users except current user and existing friends"""
    try:
        # Get IDs of current user's friends
        friendships = Friendship.query.filter_by(user_id=current_user.id).all()
        friend_ids = [f.friend_id for f in friendships]
        
        # Get IDs of users with pending friend requests (sent or received)
        sent_requests = FriendRequest.query.filter_by(
            sender_id=current_user.id, 
            status='pending'
        ).all()
        received_requests = FriendRequest.query.filter_by(
            recipient_id=current_user.id, 
            status='pending'
        ).all()
        
        pending_user_ids = [r.recipient_id for r in sent_requests] + [r.sender_id for r in received_requests]
        
        # Combine all IDs to exclude
        exclude_ids = friend_ids + pending_user_ids + [current_user.id]
        
        # Get all onboarded users except excluded ones
        users = User.query.filter(
            and_(
                User.is_onboarded == True,
                ~User.id.in_(exclude_ids)
            )
        ).all()
        
        # Return array directly for frontend compatibility
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
      
def search_users_controller(query_param, current_user):
    """Search users by name or email"""
    try:
      
      if not query_param:
        return jsonify({'message': 'Query parameter is required'}), 400
      search = f"%{query_param}%"
      users = User.query.filter(
        and_(
          User.id != current_user.id,
          or_(
            User.full_name.ilike(search),
            User.learning_language.ilike(search)
          )
        )
      ).all()
      return jsonify({
        'success': True,
        'users': [user.to_dict() for user in users]
      }), 200
    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500

def get_user_profile_controller(user_id, current_user):
    """Get user profile by ID"""
    try:
      user = User.query.get(user_id)
      if not user:
        return jsonify({'message': 'User not found'}), 404
      
      #Check friends ship status
      is_friend = Friendship.query.filter(
        or_(
          and_(Friendship.user_id == current_user.id, Friendship.friend_id == user.id),
          and_(Friendship.user_id == user.id, Friendship.friend_id == current_user.id)
        )
      ).first() is not None
      
      #Check pending friend request
      pending_request = FriendRequest.query.filter(
        or_(
          and_(
                    FriendRequest.sender_id == current_user.id,
                    FriendRequest.recipient_id == user.id,
                    FriendRequest.status == 'pending'
                ),
                and_(
                    FriendRequest.sender_id == user.id,
                    FriendRequest.recipient_id == current_user.id,
                    FriendRequest.status == 'pending'
                )
          
        )
      ).first() is not None
      
      user_data = user.to_dict()
      user_data['isFriend'] = is_friend
      user_data['hasPendingRequest'] = pending_request
      return jsonify({
        'success': True,
        'user': user_data
      }), 200
    except Exception as e:
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
      
def send_friend_request_controller(recipient_id,current_user):
    """Send a friend request"""
    try:
      if current_user.id == recipient_id:
            return jsonify({'message': 'Cannot send friend request to yourself'}), 400
        
      recipient = User.query.get(recipient_id)
      if not recipient:
        return jsonify({'message': 'User not found'}), 404
      
      # Check if already friends
      existing_friendship = Friendship.query.filter(
            or_(
                and_(Friendship.user_id == current_user.id, Friendship.friend_id == recipient_id),
                and_(Friendship.user_id == recipient_id, Friendship.friend_id == current_user.id)
            )
        ).first()
      if existing_friendship:
          return jsonify({'message': 'You are already friends'}), 400
      
      # Check for existing pending request from current user to recipient
      existing_request = FriendRequest.query.filter(
            and_(
                FriendRequest.sender_id == current_user.id,
                FriendRequest.recipient_id == recipient_id,
                FriendRequest.status == 'pending'
            )
        ).first()
      if existing_request:
          return jsonify({'message': 'You already sent a friend request to this user'}), 400
      
      # Check if recipient already sent a request to current user (mutual request)
      reverse_request = FriendRequest.query.filter(
            and_(
                FriendRequest.sender_id == recipient_id,
                FriendRequest.recipient_id == current_user.id,
                FriendRequest.status == 'pending'
            )
        ).first()
      
      # If there's a mutual request, auto-accept and create friendship
      if reverse_request:
          reverse_request.status = 'accepted'
          
          # Ensure both users exist in Stream
          from src.utils.stream import upsert_stream_user
          upsert_stream_user({
              "id": str(current_user.id),
              "name": current_user.full_name,
              "image": current_user.profile_pic or '',
          })
          upsert_stream_user({
              "id": str(recipient_id),
              "name": recipient.full_name,
              "image": recipient.profile_pic or '',
          })
          
          # Create bidirectional friendship
          friendship1 = Friendship(user_id=current_user.id, friend_id=recipient_id)
          friendship2 = Friendship(user_id=recipient_id, friend_id=current_user.id)
          
          db.session.add(friendship1)
          db.session.add(friendship2)
          db.session.commit()
          
          return jsonify({
            'success': True,
            'message': 'Friend request automatically accepted! You are now friends.',
            'friendRequest': reverse_request.to_dict()
          }), 200
      
      # Create new friend request
      friend_request = FriendRequest(
        sender_id = current_user.id,
        recipient_id = recipient_id
      )
      db.session.add(friend_request)
      db.session.commit()
      
      return jsonify({
        'success': True,
        'friendRequest': friend_request.to_dict()
      }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
      
def accept_friend_request_controller(request_id, current_user):
  try:
    friend_request = FriendRequest.query.get(request_id)
    
    if not friend_request:
      return jsonify({'message': 'Friend request not found'}), 404
    
    if friend_request.recipient_id != current_user.id:
      return jsonify({'message': 'Not authorized to accept this friend request'}), 403
    
    if friend_request.status == 'accepted':
      return jsonify({'message': 'Friend request already accepted'}), 400
    
    # Update request status
    friend_request.status = 'accepted'
    
    # Ensure both users exist in Stream
    from src.utils.stream import upsert_stream_user
    sender = User.query.get(friend_request.sender_id)
    recipient = User.query.get(friend_request.recipient_id)
    
    if sender:
        upsert_stream_user({
            "id": str(sender.id),
            "name": sender.full_name,
            "image": sender.profile_pic or '',
        })
    if recipient:
        upsert_stream_user({
            "id": str(recipient.id),
            "name": recipient.full_name,
            "image": recipient.profile_pic or '',
        })
    
    # Create bidirectional friendship
    friendship1 = Friendship(user_id=friend_request.sender_id, friend_id=friend_request.recipient_id)
    friendship2 = Friendship(user_id=friend_request.recipient_id, friend_id=friend_request.sender_id)
    
    db.session.add(friendship1)
    db.session.add(friendship2)
    db.session.commit()
    
    return jsonify({
      'success': True,
      'friendRequest': friend_request.to_dict()
    }), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
  
def get_friend_requests_controller(current_user):
  """Get pending and accepted friend requests for current user"""
  try:
    # Get incoming pending requests (where current user is recipient)
    incoming_requests = FriendRequest.query.filter_by(
      recipient_id=current_user.id, 
      status='pending'
    ).all()
    
    # Get accepted requests (where current user was sender)
    accepted_requests = FriendRequest.query.filter_by(
      sender_id=current_user.id,
      status='accepted'
    ).all()
    
    return jsonify({
      'incomingReqs': [req.to_dict() for req in incoming_requests],
      'acceptedReqs': [req.to_dict() for req in accepted_requests]
    }), 200
  except Exception as e:
    return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
  
def get_friends_controller(current_user):
  """Get friends of current user"""
  try:
    friendships = Friendship.query.filter_by(user_id=current_user.id).all()
    friends = [User.query.get(f.friend_id).to_dict() for f in friendships]
    # Return array directly for frontend compatibility
    return jsonify(friends), 200
  except Exception as e:
    return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500

def get_outgoing_friend_requests_controller(current_user):
  """Get outgoing friend requests sent by current user"""
  try:
    requests = FriendRequest.query.filter_by(sender_id=current_user.id, status='pending').all()
    # Return array directly for frontend compatibility
    return jsonify([req.to_dict() for req in requests]), 200
  except Exception as e:
    return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500