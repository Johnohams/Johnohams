from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager # Import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager() # Initialize JWTManager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev_secret_key' # Used for signing JWTs too
    app.config['JWT_SECRET_KEY'] = 'jwt-dev-secret-key' # Separate JWT secret key is good practice

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app) # Initialize JWTManager with the app

    from app import models

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.messaging import messaging_bp # Import the messaging blueprint
    app.register_blueprint(messaging_bp)   # Register the blueprint

    return app
