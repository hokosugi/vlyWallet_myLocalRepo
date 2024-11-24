from dotenv import load_dotenv
import os
from flask import Flask, request, session
from database import db
import logging
from sqlalchemy.exc import SQLAlchemyError
from flask_babel import Babel
from flask_login import LoginManager
from models import db, Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



load_dotenv()
print(f"ADMIN_PASSWORD set: {'ADMIN_PASSWORD' in os.environ}")
# db = SQLAlchemy()
migrate = Migrate()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

login_manager = LoginManager()

def get_locale():
    return session.get('lang', 'en')

def create_app():
    flask_app = Flask(__name__)
    # flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ueyamamasashi@localhost/postgres'
    # flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # migrate = Migrate(flask_app, db)

    # Configure Flask app
    flask_app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
    flask_app.debug = True

    # Initialize Babel
    babel = Babel(flask_app, locale_selector=get_locale)

    # Initialize Login Manager
    login_manager.init_app(flask_app)
    login_manager.login_view = 'admin_login'

    # Database configuration with error handling
    try:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            logger.error("DATABASE_URL environment variable not set!")
            raise ValueError("DATABASE_URL must be set")
        
        logger.debug(f"Configuring database with URL: {database_url}")
        
        # Configure SQLAlchemy
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        flask_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_size": 5,
            "max_overflow": 2,
            "pool_timeout": 30,
            "pool_recycle": 300,
            "pool_pre_ping": True,
        }
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        db.init_app(flask_app)
        migrate.init_app(flask_app, db)

        with flask_app.app_context():
            # Import models and views after app initialization
            from models import User, Transaction, Admin
            from views import register_routes
            from scheduler import run_update_transactions
            from scheduler import start_scheduler
            
            @login_manager.user_loader
            def load_user(user_id):
                return Admin.query.get(int(user_id))
            
            try:
                # Test database connection
                db.engine.connect()
                logger.info("Successfully connected to database")
                
                # Create database tables
                db.create_all()
                logger.info("Database tables created successfully")
                
                # Remove existing admin if exists
                Admin.query.filter_by(username='admin').delete()
                db.session.commit()
                logger.info("Existing admin user removed")

                # Get admin password from environment variable
                admin_password = os.environ.get('ADMIN_PASSWORD')
                if not admin_password:
                    logger.error("ADMIN_PASSWORD environment variable not set!")
                    raise ValueError("ADMIN_PASSWORD must be set")

                # Create new admin user with environment variable password
                admin = Admin(username='admin')
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                logger.info("Default admin user created/reset with environment password")
                
                # Start scheduler for a day updates
                start_scheduler(run_update_transactions)
                logger.info("Transaction update scheduler started")
                
            except SQLAlchemyError as e:
                logger.error(f"Database error occurred: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Error during application setup: {str(e)}")
                raise
            
            # Register routes
            register_routes(flask_app)
            logger.info("Routes registered successfully")
    
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise


    def index():
        return "Welcome to VlyWallet Leaderboard"
    return flask_app

flask_app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask application...")
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
