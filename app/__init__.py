from flask import Flask
from flask_mongoengine import MongoEngine

from .config import Config

db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
