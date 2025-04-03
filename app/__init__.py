import sentry_sdk
from flask import Flask
from flask_mongoengine import MongoEngine
from sentry_sdk.integrations.flask import FlaskIntegration

from .config import Config

db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoEngine with Flask app
    db.init_app(app)

    # Initialize Sentry for error monitoring and logging
    sentry_sdk.init(
        dsn="https://491d31c12ffd3d7e9f9607fd4f475b9b@o4509086856118272.ingest.us.sentry.io/4509086879842304",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,  # Adjust based on performance requirements
    )

    # Register blueprints/routes
    from .routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
