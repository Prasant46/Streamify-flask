from datetime import datetime
from src.extensions import db

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('sender_id', 'recipient_id', name='unique_friend_request'),
        db.CheckConstraint(status.in_(['pending', 'accepted']), name='valid_status'),
        db.Index('idx_recipient_status', 'recipient_id', 'status'),
    )
    
    def to_dict(self):
        return {
            '_id': str(self.id),
            'id': self.id,
            'senderId': self.sender_id,
            'recipientId': self.recipient_id,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'sender': self.sender.to_dict() if self.sender else None,
            'recipient': self.recipient.to_dict() if self.recipient else None
        }
    
    def __repr__(self):
        return f'<FriendRequest {self.sender_id} -> {self.recipient_id} ({self.status})>'