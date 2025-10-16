import os
from flask_migrate import Migrate, init, migrate, upgrade
from src.app import create_app
from src.extensions import db

app = create_app(os.getenv('FLASK_ENV', 'development'))
migrate_obj = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")