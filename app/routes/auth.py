from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
# We'll need to add JWT later if we go that route
from flask_jwt_extended import create_access_token # Import create_access_token

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing username, email, or password'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409 # 409 Conflict

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email address already registered'}), 409

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or (not data.get('username') and not data.get('email')) or not data.get('password'):
        return jsonify({'message': 'Missing username/email or password'}), 400

    user = None
    if data.get('username'):
        user = User.query.filter_by(username=data['username']).first()
    elif data.get('email'):
        user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username/email or password'}), 401

    # For now, just a success message. JWT can be added here later.
    access_token = create_access_token(identity=user.id) # Create JWT
    return jsonify(access_token=access_token), 200 # Return JWT
