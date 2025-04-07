# File: app/config.py
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    MONGODB_SETTINGS = {
        "host": os.getenv("MONGODB_URI"),
        "db": "ah-aihms-db",
        "tls": True,
        "uuidRepresentation": "standard",  # ✅ resolves deprecation warning
    }
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes (in seconds)
    JWT_REFRESH_TOKEN_EXPIRES = 604800  # 7 days (in seconds)

    # Flask-Mail Configuration (local development / production)
    # For local testing you may use Gmail or a local SMTP server.
    # For production with SendGrid, set the following environment variables accordingly.
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "1", "yes"]
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ["true", "1", "yes"]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # OAuth Configuration for Google
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    # Allow HTTP for local development (remove in production)
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv("OAUTHLIB_INSECURE_TRANSPORT", "1")
