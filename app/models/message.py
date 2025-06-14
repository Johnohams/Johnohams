from app import db # Assuming db is initialized in app/__init__.py
from datetime import datetime, timezone # Use timezone-aware datetimes

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text, nullable=False) # Will consider encrypting this later
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    read_status = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id} to {self.recipient_id}>'
