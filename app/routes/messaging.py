from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.message import Message
from sqlalchemy import or_ # Import 'or_' for combined queries

messaging_bp = Blueprint('messaging_bp', __name__, url_prefix='/messages')

@messaging_bp.route('/send', methods=['POST'])
@jwt_required() # Protect this route
def send_message():
    current_user_id = get_jwt_identity() # Get sender's ID from JWT
    data = request.get_json()

    if not data or not data.get('recipient_id') or not data.get('body'):
        return jsonify({'message': 'Missing recipient_id or message body'}), 400

    recipient_id = data.get('recipient_id')
    body = data.get('body')

    # Check if recipient exists
    recipient = User.query.get(recipient_id)
    if not recipient:
        return jsonify({'message': 'Recipient user not found'}), 404

    # Prevent sending messages to oneself (optional, but common)
    # Ensure recipient_id is integer for comparison if current_user_id is int
    try:
        if int(current_user_id) == int(recipient_id): # Make sure types are consistent
                return jsonify({'message': 'Cannot send message to yourself'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    message = Message(sender_id=current_user_id, recipient_id=recipient_id, body=body)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully', 'message_id': message.id}), 201

@messaging_bp.route('/list', methods=['GET']) # New endpoint
@jwt_required()
def list_messages():
    current_user_id = get_jwt_identity()

    # Retrieve messages where the current user is either the sender or recipient
    # Order by timestamp descending (newest first)
    messages = Message.query.filter(
        or_(Message.sender_id == current_user_id, Message.recipient_id == current_user_id)
    ).order_by(Message.timestamp.desc()).all()

    output = []
    for message in messages:
        output.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'recipient_id': message.recipient_id,
            'body': message.body, # Note: In a real app, consider if body should always be returned or if there's an 'unread' summary
            'timestamp': message.timestamp.isoformat(), # Use ISO format for dates
            'read_status': message.read_status
        })

    return jsonify(messages=output), 200
