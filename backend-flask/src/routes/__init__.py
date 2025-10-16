from src.routes.auth_routes import auth_bp
from src.routes.user_routes import user_bp
from src.routes.chat_routes import chat_bp

def register_routes(app):
    """Register all blueprints with /api prefix to match frontend"""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')