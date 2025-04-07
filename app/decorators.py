# File: app/decorators.py
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(*roles):
    """
    Decorator to restrict access to endpoints based on user roles.
    Usage: @role_required('admin', 'doctor')
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"msg": "Insufficient privileges"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
