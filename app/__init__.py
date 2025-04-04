import logging
import os

import sentry_sdk
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from sentry_sdk.integrations.flask import FlaskIntegration

from .config import Config

# Instantiate the MongoEngine connection object (used by models).
db = MongoEngine()

# Configure Python's built-in logging at module level (typical for production apps).
# You can also configure more complex loggers and handlers as needed.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """
    Factory function to create and configure the Flask application.

    1. Loads configuration from `Config`.
    2. Initializes database connection (MongoEngine).
    3. Registers Sentry for error monitoring.
    4. Registers blueprints, routes, and global error handlers.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoEngine with the Flask app
    db.init_app(app)

    # Initialize Sentry for error monitoring and logging
    sentry_sdk.init(
        dsn="https://491d31c12ffd3d7e9f9607fd4f475b9b@o4509086856118272.ingest.us.sentry.io/4509086879842304",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,  # Adjust based on performance requirements
    )

    # Register blueprints/routes here
    from .routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Register error handlers after blueprints
    register_error_handlers(app)

    # Log startup info
    logger.info("Flask application has been created and configured successfully.")
    logger.info("Environment: %s", os.getenv("FLASK_ENV", "development"))
    return app


def register_error_handlers(app: Flask):
    """
    Registers global error handlers for common HTTP error codes and
    unexpected exceptions. Returns JSON responses and appropriate
    status codes. Production apps often keep these in a separate file
    if they become more extensive.
    """

    @app.errorhandler(404)
    def handle_not_found(e):
        """
        Handle resource not found (HTTP 404).
        Returns a JSON payload with a human-readable message.
        """
        logger.warning("404 Not Found: %s", e)
        response = {
            "error": "Not Found",
            "message": "The requested resource was not found on this server.",
        }
        return jsonify(response), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """
        Handle method not allowed (HTTP 405).
        """
        logger.warning("405 Method Not Allowed: %s", e)
        response = {
            "error": "Method Not Allowed",
            "message": "The requested method is not allowed for this endpoint.",
        }
        return jsonify(response), 405

    @app.errorhandler(500)
    def handle_internal_error(e):
        """
        Handle generic server error (HTTP 500).
        Flask will invoke this if code raises a 500 (e.g., an unhandled exception).
        Sentry also captures the error automatically.
        """
        logger.error("500 Internal Server Error: %s", e, exc_info=True)
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error has occurred on the server.",
        }
        return jsonify(response), 500

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        """
        Catch-all for any uncaught exceptions.
        This ensures we log them for debugging and return a consistent JSON response.
        """
        logger.error("Unhandled Exception: %s", e, exc_info=True)
        response = {
            "error": "Server Error",
            "message": "An unexpected exception has occurred.",
        }
        return jsonify(response), 500
