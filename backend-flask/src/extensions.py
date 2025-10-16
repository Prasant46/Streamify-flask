from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def init_extensions(app):
    """Initialize Flask extensions with proper CORS configuration"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Configure CORS to allow requests from frontend
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:5173", "http://localhost:3000"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Accept"],
                "supports_credentials": True,
                "expose_headers": ["Content-Type", "Authorization"],
                "max_age": 3600
            }
        }
    )