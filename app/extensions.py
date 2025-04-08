# app/extensions.py
"""
Initialize Flask extensions and OAuth providers.

Environment Variables:
- SECRET_KEY: Base secret key for Flask sessions and token signing.
- JWT_SECRET_KEY: Secret key for JWT tokens (if not provided, uses SECRET_KEY).
- JWT_ACCESS_TOKEN_EXPIRES: (optional) Access token expiration (in seconds, e.g. 900 for 15 min).
- JWT_REFRESH_TOKEN_EXPIRES: (optional) Refresh token expiration (e.g. 2592000 for 30 days).
- MAIL_SERVER: SMTP server (e.g., 'smtp.gmail.com' or 'smtp.sendgrid.net').
- MAIL_PORT: SMTP port (e.g., 587).
- MAIL_USE_TLS: Enable TLS (True/False).
- MAIL_USE_SSL: Enable SSL (True/False).
- MAIL_USERNAME: SMTP username (for Gmail or SendGrid, e.g., 'apikey' for SendGrid).
- MAIL_PASSWORD: SMTP password or API key (for SendGrid, use the API key as password).
- MAIL_DEFAULT_SENDER: Default "From" email address for outgoing emails.
- SENDGRID_API_KEY: (optional) SendGrid API key (if using SendGrid Web API instead of SMTP).
- GOOGLE_CLIENT_ID: Google OAuth Client ID.
- GOOGLE_CLIENT_SECRET: Google OAuth Client Secret.
"""
import os

from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_mail import Mail

# Instantiate extensions
jwt = JWTManager()
mail = Mail()
oauth = OAuth()


def init_extensions(app):
    """
    Initialize Flask extensions and configure Google OAuth client.
    """
    jwt.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    if client_id and client_secret:
        oauth.register(
            name="google",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
        app.logger.info("✅ Google OAuth client registered.")
    else:
        app.logger.warning("⚠️ Google OAuth credentials not set. Skipping OAuth registration.")
