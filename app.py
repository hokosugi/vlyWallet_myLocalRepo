import os
from flask import Flask
from database import db
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    flask_app = Flask(__name__)
    
    # Configure Flask app
    flask_app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
    flask_app.debug = True
    
    # Database configuration with error handling
    try:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            logger.error("DATABASE_URL environment variable not set!")
            raise ValueError("DATABASE_URL must be set")
        
        logger.debug(f"Configuring database with URL: {database_url.split('@')[1]}")
        
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
        
        # Initialize database
        db.init_app(flask_app)
        
        with flask_app.app_context():
            # Import models and views after app initialization
            from models import User, Transaction
            from views import register_routes
            from vly_api import update_transactions
            from scheduler import start_scheduler
            
            try:
                # Test database connection
                db.engine.connect()
                logger.info("Successfully connected to database")
                
                # Create database tables
                db.create_all()
                logger.info("Database tables created successfully")
                
                # Start scheduler for weekly updates
                start_scheduler(update_transactions)
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
    
    return flask_app

app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask application...")
    app.run(host="0.0.0.0", port=5000, debug=True)
