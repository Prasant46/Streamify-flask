from datetime import datetime, timezone
from src.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  bio = db.Column(db.Text, default='')
  profile_pic = db.Column(db.String(255), default='')
  native_language = db.Column(db.String(50), default='')
  learning_language = db.Column(db.String(50), default='')
  location = db.Column(db.String(255), default='')
  is_onboarded = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))
  
  
  #Relationships
  sent_requests = db.relationship(
    'FriendRequest', 
    foreign_keys='FriendRequest.sender_id', backref='sender', 
    lazy='dynamic',
    cascade='all, delete-orphan'
  )
  
  received_requests = db.relationship(
    'FriendRequest',
    foreign_keys='FriendRequest.recipient_id', backref='recipient', 
    lazy='dynamic',
    cascade='all, delete-orphan'
  )
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def get_friends(self):
    """Get all friends of this user"""
    friendships = Friendship.query.filter_by(user_id=self.id).all()
    return [User.query.get(f.friend_id) for f in friendships]
  
  def to_dict(self, include_email=True):
    data = {
      '_id': str(self.id),
      'fullName': self.full_name,
      'bio': self.bio,
      'profilePic': self.profile_pic,
      'nativeLanguage': self.native_language,
      'learningLanguage': self.learning_language,
      'location': self.location,
      'isOnboarded': self.is_onboarded,
      'createdAt': self.created_at.isoformat() if self.created_at else None
    }
    
    if include_email:
      data['email'] = self.email
    return data
  
  def __repr__(self):
    return f'<User {self.email}>'
  
class Friendship(db.Model):
  __tablename__ = 'friends'
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
  friend_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
  created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))
  
  __table_args__ = (
    db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    db.Index('idx_user_friend', 'user_id', 'friend_id')
  )
  
  def __repr__(self):
    return f'<Friendship user_id={self.user_id} friend_id={self.friend_id}>'