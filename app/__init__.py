from flask import Flask

from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
