# File: app/__init__.py
import logging
import os

import sentry_sdk
from flask import Flask
from flask_mongoengine import MongoEngine
from sentry_sdk.integrations.flask import FlaskIntegration

from .config import Config
from .extensions import init_extensions  # import db and init_extensions

# Initialize MongoEngine for database interactions
db = MongoEngine()

# Configure Python's built-in logging for production use.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Factory function to create and configure the Flask application.

    Steps:
      1. Load configuration from Config.
      2. Initialize the MongoDB connection via MongoEngine.
      3. Configure Sentry for error monitoring.
      4. Initialize third-party extensions: JWT, Mail, and OAuth.
      5. Register blueprints (e.g., authentication routes).
      6. Register global error handlers.
      7. Log startup information.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    assert app.config["MONGODB_SETTINGS"]["host"], "❌ MONGODB_URI is missing or not loaded!"

    # Initialize MongoEngine with the Flask app
    db.init_app(app)

    # Initialize Sentry for error monitoring and logging.
    # Replace the DSN below with your actual Sentry DSN in production.
    sentry_sdk.init(
        dsn="https://491d31c12ffd3d7e9f9607fd4f475b9b@o4509086856118272.ingest.us.sentry.io/4509086879842304",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )

    # ✅ Initialize all extensions, including OAuth
    init_extensions(app)

    # Register application blueprints (e.g., auth routes)
    from .routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Register global error handlers (from a separate module for clarity)
    from .register_error_handlers import register_error_handlers

    register_error_handlers(app)

    # Log startup information
    logger.info("Flask application created and configured.")
    logger.info("Environment: %s", os.getenv("FLASK_ENV", "development"))

    return app
