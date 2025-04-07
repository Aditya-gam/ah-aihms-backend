# File: app/routes/auth.py
"""
Authentication and Authorization Routes

This module defines endpoints for:
  - User Registration (for 'patient' or 'doctor' roles)
  - Email Verification for account activation
  - Login with JWT issuance and optional Two-Factor Authentication (2FA) via email OTP
  - Token Refresh endpoint to renew access tokens
  - Password Reset (request and reset endpoints)
  - Google OAuth integration (via Authlib) for login/registration

Dependencies:
  - Flask and Flask-JWT-Extended for routing and JWT management.
  - itsdangerous for secure token generation and confirmation.
  - bcrypt for password hashing.
  - Flask-Mail for sending emails.
  - Authlib for OAuth support.
  - MongoEngine for database interactions.
"""

import random
import string
from datetime import UTC, datetime, timedelta

import bcrypt
from flask import Blueprint, current_app, jsonify, request, url_for
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.extensions import mail, oauth
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# Error messages
USER_NOT_FOUND_MSG = "User not found."

# In-memory store for 2FA codes (for demonstration purposes only).
# For production, use a persistent store (e.g., Redis) with expiration.
two_factor_store = {}


def generate_token(email: str, salt: str) -> str:
    """
    Generate a secure token for email verification or password reset.

    Args:
        email (str): The user's email address.
        salt (str): Salt value to differentiate token types(e.g., "email-confirm", "password-reset")

    Returns:
        str: The generated token.
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=salt)


def confirm_token(token: str, salt: str, expiration: int = 3600) -> str | None:
    """
    Confirm the token's validity and retrieve the associated email.

    Args:
        token (str): The token to validate.
        salt (str): The salt used during token generation.
        expiration (int, optional): Token validity period in seconds (default is 3600).

    Returns:
        str | None: The email if valid; otherwise, None.
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    return email


def send_email(subject: str, recipients: list, body: str) -> None:
    """
    Send an email using Flask-Mail.

    Args:
        subject (str): Email subject line.
        recipients (list): List of recipient email addresses.
        body (str): Plain text email body.
    """
    from flask_mail import Message

    msg = Message(subject=subject, recipients=recipients, body=body)
    mail.send(msg)


@auth_bp.route("/status", methods=["GET"])
def status():
    """
    Health check endpoint to confirm that the authentication routes are operational.

    Returns:
        JSON response with the status message.
    """
    return jsonify({"status": "auth route working"}), 200


@auth_bp.route("/register/<role>", methods=["POST"])
def register(role: str):
    """
    Register a new user with a specified role ('patient' or 'doctor').

    Expects JSON payload with:
      - email
      - password
      - first_name
      - last_name
      - phone_number
      - address
      - emergency_contact

    Args:
        role (str): The role for the new user.

    Returns:
        JSON response indicating success or failure.
    """
    if role not in ["patient", "doctor"]:
        return jsonify({"msg": "Invalid role specified."}), 400

    data = request.get_json()
    required_fields = [
        "email",
        "password",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "emergency_contact",
    ]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields."}), 400

    if User.objects(email=data["email"]).first():
        return jsonify({"msg": "User with this email already exists."}), 400

    # Hash the password using bcrypt.
    password_bytes = data["password"].encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    # Create the user instance.
    user = User(
        email=data["email"],
        password_hash=hashed,
        role=role,
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone_number=data["phone_number"],
        address=data["address"],
        emergency_contact=data["emergency_contact"],
    )
    try:
        user.save()
    except Exception as e:
        return jsonify({"msg": "Error creating user", "error": str(e)}), 500

    # Generate and send email verification token.
    token = generate_token(user.email, salt="email-confirm")
    verification_link = url_for("auth.verify_email", token=token, _external=True)
    subject = "Verify Your Email"
    body = (
        f"Hi {user.first_name},\n\n"
        f"Please verify your email by clicking the link below:\n{verification_link}\n\n"
        "If you did not sign up, please ignore this email."
    )
    try:
        send_email(subject, [user.email], body)
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email: {e}")

    return (
        jsonify({"msg": "Registration successful. Check your email to verify your account."}),
        201,
    )


@auth_bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token: str):
    """
    Verify the user's email using the provided token.

    Args:
        token (str): The email verification token.

    Returns:
        JSON response indicating the verification status.
    """
    email = confirm_token(token, salt="email-confirm")
    if not email:
        return jsonify({"msg": "Verification link is invalid or expired."}), 400

    user = User.objects(email=email).first()
    if not user:
        return jsonify({"msg": USER_NOT_FOUND_MSG}), 404

    if user.verified:
        return jsonify({"msg": "Account already verified."}), 200

    user.verified = True
    user.save()
    return jsonify({"msg": "Email verified successfully."}), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate the user and issue JWT tokens.

    Expects JSON payload with:
      - email
      - password

    If two-factor authentication is enabled for the user, an OTP is sent via email,
    and the endpoint instructs the user to verify the OTP.

    Returns:
        JSON response with access and refresh tokens, or 2FA instructions.
    """
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"msg": "Email and password required."}), 400

    user = User.objects(email=data["email"]).first()
    if not user or not bcrypt.checkpw(
        data["password"].encode("utf-8"), user.password_hash.encode("utf-8")
    ):
        return jsonify({"msg": "Invalid credentials."}), 401

    if not user.verified:
        return jsonify({"msg": "Email not verified. Please verify your email."}), 403

    # If 2FA is enabled, generate and send a one-time password (OTP).
    if user.two_factor_enabled:
        otp = "".join(random.choices(string.digits, k=6))
        two_factor_store[user.email] = {
            "otp": otp,
            "expires_at": datetime.now(UTC) + timedelta(minutes=5),
        }
        subject = "Your 2FA Code"
        body = f"Your Two-Factor Authentication code is: {otp}"
        try:
            send_email(subject, [user.email], body)
        except Exception as e:
            current_app.logger.error(f"Failed to send 2FA email: {e}")
            return jsonify({"msg": "Failed to send 2FA code."}), 500
        return jsonify({"msg": "2FA code sent to your email. Verify to complete login."}), 200

    # Issue JWT tokens with additional claims (e.g., user role).
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.route("/verify-2fa", methods=["POST"])
def verify_2fa():
    """
    Verify the OTP provided for two-factor authentication and issue JWT tokens.

    Expects JSON payload with:
      - email
      - otp

    Returns:
        JSON response with JWT tokens upon successful OTP verification.
    """
    data = request.get_json()
    if not data or "email" not in data or "otp" not in data:
        return jsonify({"msg": "Email and OTP required."}), 400

    record = two_factor_store.get(data["email"])
    if not record:
        return jsonify({"msg": "No 2FA request found. Please login again."}), 400

    if datetime.now(UTC) > record["expires_at"]:
        del two_factor_store[data["email"]]
        return jsonify({"msg": "OTP expired. Please login again."}), 400

    if data["otp"] != record["otp"]:
        return jsonify({"msg": "Invalid OTP."}), 400

    # Clear the OTP record after successful verification.
    del two_factor_store[data["email"]]

    user = User.objects(email=data["email"]).first()
    if not user:
        return jsonify({"msg": USER_NOT_FOUND_MSG}), 404

    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def token_refresh():
    """
    Refresh the access token using a valid refresh token.

    Returns:
        JSON response containing the new access token.
    """
    identity = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {"role": claims.get("role")}
    new_access = create_access_token(identity=identity, additional_claims=additional_claims)
    return jsonify({"access_token": new_access}), 200


@auth_bp.route("/password-reset-request", methods=["POST"])
def password_reset_request():
    """
    Initiate a password reset by sending an email with a reset link.

    Expects JSON payload with:
      - email

    Returns:
        JSON response indicating that if the email exists, a reset link will be sent.
    """
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"msg": "Email required."}), 400

    user = User.objects(email=data["email"]).first()
    if user:
        token = generate_token(user.email, salt="password-reset")
        reset_link = url_for("auth.password_reset", token=token, _external=True)
        subject = "Password Reset Request"
        body = (
            f"Hi {user.first_name},\n\n"
            f"Reset your password by clicking the link below:\n{reset_link}\n\n"
            "This link is valid for 1 hour. Ignore if not requested."
        )
        try:
            send_email(subject, [user.email], body)
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset email: {e}")
    return jsonify({"msg": "If the email exists, a password reset link will be sent."}), 200


@auth_bp.route("/password-reset/<token>", methods=["POST"])
def password_reset(token: str):
    """
    Reset the user's password after validating the reset token.

    Expects JSON payload with:
      - new_password

    Args:
        token (str): The password reset token.

    Returns:
        JSON response indicating success or failure of the password reset.
    """
    email = confirm_token(token, salt="password-reset")
    if not email:
        return jsonify({"msg": "Reset link is invalid or expired."}), 400

    data = request.get_json()
    if not data or "new_password" not in data:
        return jsonify({"msg": "New password required."}), 400

    user = User.objects(email=email).first()
    if not user:
        return jsonify({"msg": USER_NOT_FOUND_MSG}), 404

    new_password_bytes = data["new_password"].encode("utf-8")
    new_hashed = bcrypt.hashpw(new_password_bytes, bcrypt.gensalt()).decode("utf-8")
    user.password_hash = new_hashed
    user.save()
    return jsonify({"msg": "Password reset successful."}), 200


@auth_bp.route("/oauth/google", methods=["GET"])
def oauth_google():
    """
    Initiate the Google OAuth flow by redirecting to Google's OAuth consent screen.

    Returns:
        A redirection to the Google OAuth authorization URL.
    """
    redirect_uri = url_for("auth.oauth_google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route("/oauth/google/callback", methods=["GET"])
def oauth_google_callback():
    """
    Handle the Google OAuth callback by obtaining user info and logging in or registering the user.

    Returns:
        JSON response containing JWT tokens upon successful authentication.
    """
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    if not user_info:
        return jsonify({"msg": "Failed to fetch user info from Google."}), 400

    email = user_info.get("email")
    if not email:
        return jsonify({"msg": "Google account does not provide an email."}), 400

    # Look for an existing user; if not found, create a new one with default role 'patient'
    user = User.objects(email=email).first()
    if not user:
        user = User(
            email=email,
            password_hash="",  # OAuth users do not have a local password.
            role="patient",
            first_name=user_info.get("given_name", ""),
            last_name=user_info.get("family_name", ""),
            phone_number="",
            address="",
            emergency_contact={"name": "", "relationship": "", "phone_number": ""},
            verified=True,
            oauth_provider="google",
            oauth_id=user_info.get("sub"),
        )
        user.save()

    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
