# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from config import Config
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
cache = Cache()
cors = CORS()

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    cors.init_app(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    from app.api.routes import api
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    # Import models for migration tracking
    from app.models import User, Calculation

    # Create tables if not exists
    with app.app_context():
        db.create_all()

    # CLI commands
    @app.cli.command("create-admin")
    def create_admin():
        """Create admin user"""
        from app.models import User
        admin = User(
            username=os.getenv('ADMIN_USER', 'admin'),
            email=os.getenv('ADMIN_EMAIL', 'admin@prp.com'),
            employee_id='ADMIN001',
            grade='ADMIN',
            department='IT'
        )
        admin.set_password(os.getenv('ADMIN_PASS', 'admin123'))
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app